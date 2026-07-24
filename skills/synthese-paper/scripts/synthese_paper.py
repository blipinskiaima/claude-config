#!/usr/bin/env python3
"""Synthèse d'un article scientifique, strictement identique à celle d'Aima-Tower /survey.

Fidélité garantie par construction : le prompt système et le wrapper d'appel sont IMPORTÉS
depuis ~/Pipeline/Aima-Tower/src/ — jamais dupliqués. Si le prompt de Tower change, ce script
suit automatiquement.

Usage:
    synthese_paper.py <entrée> [--out fichier.md] [--fulltext]

Entrées acceptées : PMID, DOI, URL PubMed/DOI, chemin vers un PDF.
    --fulltext  : pour un PDF, injecte le texte intégral au lieu du seul résumé.
                  ⚠ ÉCART avec Tower (dont le prompt impose de se baser sur le résumé seul).
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

TOWER_SRC = Path("/home/blipinski/Pipeline/Aima-Tower/src")
SURVEY_DB = Path("/home/blipinski/Pipeline/Aima-Survey/data/aima_survey.duckdb")
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


# ---------- résolution de l'entrée ----------

def detect_kind(raw: str) -> str:
    if Path(raw).expanduser().is_file():
        return "pdf"
    if re.fullmatch(r"\d{6,9}", raw.strip()):
        return "pmid"
    if raw.startswith("10.") or "doi.org/" in raw:
        return "doi"
    if raw.startswith("http"):
        return "url"
    raise SystemExit(f"Entrée non reconnue : {raw}")


def _get(url: str, params: dict) -> str:
    import os

    import requests
    key = os.environ.get("NCBI_API_KEY")
    if key:
        params = {**params, "api_key": key}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.text


def pmid_from_doi(doi: str) -> str | None:
    doi = doi.split("doi.org/")[-1].strip()
    xml = _get(f"{EUTILS}/esearch.fcgi", {"db": "pubmed", "term": f"{doi}[DOI]", "retmode": "xml"})
    ids = ET.fromstring(xml).findall(".//Id")
    return ids[0].text if ids else None


def fetch_pubmed(pmid: str) -> dict:
    xml = _get(f"{EUTILS}/efetch.fcgi", {"db": "pubmed", "id": pmid, "retmode": "xml"})
    node = ET.fromstring(xml).find(".//PubmedArticle")
    if node is None:
        raise SystemExit(f"PMID {pmid} introuvable.")

    abs_nodes = node.findall(".//Abstract/AbstractText")
    abstract = " ".join(
        ((n.get("Label") + ": ") if n.get("Label") else "") + (n.text or "") for n in abs_nodes
    ).strip() or (node.findtext(".//AbstractText") or "").strip()

    authors = []
    for au in node.findall(".//Author"):
        last = (au.findtext("LastName") or "").strip()
        first = (au.findtext("ForeName") or "").strip()
        if last:
            authors.append(f"{last} {first}".strip())

    y = node.findtext(".//PubDate/Year") or ""
    m = node.findtext(".//PubDate/Month") or ""
    d = node.findtext(".//PubDate/Day") or ""

    return {
        "pmid": pmid,
        "title": (node.findtext(".//ArticleTitle") or "").strip(),
        "abstract": abstract,
        "authors": ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else ""),
        "journal": (node.findtext(".//Journal/Title") or "").strip(),
        "date": "-".join(x for x in (y, m, d) if x),
    }


def parse_pdf(path: str, fulltext: bool) -> dict:
    from pypdf import PdfReader
    pages = [(p.extract_text() or "") for p in PdfReader(path).pages]
    text = "\n".join(pages).strip()
    if not text:
        raise SystemExit("PDF sans texte extractible (scan ?). Fournir plutôt le DOI ou le PMID.")

    first = pages[0] if pages else ""
    lines = [l.strip() for l in first.splitlines() if l.strip()]
    title = max(lines[:15], key=len) if lines else Path(path).stem

    if fulltext:
        body = text
    else:
        m = re.search(r"(?is)\babstract\b[:\s]*(.{200,3000}?)(?=\n\s*(introduction|keywords|1[\.\s])|\Z)", first + "\n" + (pages[1] if len(pages) > 1 else ""))
        body = m.group(1).strip() if m else first[:2500]

    doi = None
    md = re.search(r"10\.\d{4,9}/[^\s\"'<>]+", text)
    if md:
        doi = md.group(0).rstrip(".,;")

    return {"pmid": doi or Path(path).name, "title": title, "abstract": body,
            "authors": "non précisé", "journal": "non précisé", "date": "non précisé"}


# ---------- métadonnées de veille ----------

def veille_meta(pmid: str) -> dict:
    """Récupère priorité et rubriques réelles si l'article est déjà dans la veille."""
    out = {"priority": "non classé", "categories": ["hors veille"], "score": None}
    if not SURVEY_DB.exists() or not pmid.isdigit():
        return out
    try:
        import duckdb
        con = duckdb.connect(str(SURVEY_DB), read_only=True)
        row = con.execute(
            "SELECT priority, queries_matched, score FROM articles WHERE external_id = ?", [pmid]
        ).fetchone()
        con.close()
        if row:
            out["priority"] = row[0] or "non classé"
            out["categories"] = [c.strip() for c in (row[1] or "").split(",") if c.strip()] or ["hors veille"]
            out["score"] = row[2]
    except Exception as exc:                                    # DB verrouillée par le cron
        print(f"[warn] lecture veille impossible : {exc}", file=sys.stderr)
    return out


# ---------- synthèse ----------

def build_content(a: dict, meta: dict) -> str:
    """Format IDENTIQUE à SurveyService.generate_article_synthesis."""
    return (
        f"PMID : {a['pmid']}\n"
        f"Date : {a['date']}\n"
        f"Priorité : {meta['priority'].upper()}\n"
        f"Rubriques : {', '.join(meta['categories'])}\n"
        f"Journal : {a['journal']}\n"
        f"Auteurs : {a['authors']}\n"
        f"Titre : {a['title']}\n\n"
        f"Résumé :\n{a['abstract']}"
    )


def synthesize(content: str) -> str:
    if not TOWER_SRC.is_dir():
        raise SystemExit(f"Aima-Tower introuvable ({TOWER_SRC}) — fidélité non garantie, abandon.")
    sys.path.insert(0, str(TOWER_SRC))
    from claude_cli import call_claude                                    # noqa: E402
    from prompts.survey_synthesis import (                                # noqa: E402
        SURVEY_ARTICLE_SYNTHESIS_SYSTEM_PROMPT,
    )
    return call_claude(content, SURVEY_ARTICLE_SYNTHESIS_SYSTEM_PROMPT)


def main() -> None:
    ap = argparse.ArgumentParser(description="Synthèse d'article, identique à Aima-Tower /survey.")
    ap.add_argument("entree", help="PMID, DOI, URL ou chemin PDF")
    ap.add_argument("--out", help="écrire la synthèse dans ce fichier")
    ap.add_argument("--fulltext", action="store_true",
                    help="PDF : injecter le texte intégral (ÉCART avec Tower)")
    args = ap.parse_args()

    kind = detect_kind(args.entree)
    if kind == "pdf":
        article = parse_pdf(args.entree, args.fulltext)
    else:
        if kind == "pmid":
            pmid = args.entree.strip()
        elif kind == "doi":
            pmid = pmid_from_doi(args.entree) or ""
        else:                                                             # url
            m = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", args.entree)
            pmid = m.group(1) if m else (pmid_from_doi(args.entree) or "")
        if not pmid:
            raise SystemExit("Impossible de résoudre un PMID. Fournir le PMID directement.")
        article = fetch_pubmed(pmid)

    meta = veille_meta(article["pmid"])
    print(f"[info] {article['pmid']} — {article['title'][:70]}", file=sys.stderr)
    print(f"[info] priorité={meta['priority']} rubriques={','.join(meta['categories'])}"
          + (f" score={meta['score']}" if meta["score"] is not None else ""), file=sys.stderr)
    if args.fulltext:
        print("[warn] --fulltext : ÉCART avec Tower (prompt prévu pour le résumé seul)", file=sys.stderr)

    text = synthesize(build_content(article, meta))
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"[info] écrit dans {args.out}", file=sys.stderr)
    print(text)


if __name__ == "__main__":
    main()
