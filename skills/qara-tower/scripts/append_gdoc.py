"""Ajoute un bloc de texte à la FIN d'un Google Doc, sans toucher l'existant.

Utilise les credentials gspread existants (~/.config/gspread, scope drive actif)
et l'API Google Docs `batchUpdate` / `insertText` — insertion à l'index de fin,
donc le contenu déjà présent n'est jamais réécrit.

Usage :
    python append_gdoc.py <doc_id> --text-file bloc.txt --title "QARA — 2026-08-01T…"
"""
import argparse
import sys
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qara_lib  # noqa: E402


def _token() -> str:
    creds = Credentials.from_authorized_user_file(str(qara_lib.GSPREAD_CREDS))
    if not creds.valid:
        creds.refresh(Request())
    return creds.token


def _end_index(tok: str, doc_id: str) -> int:
    r = requests.get(f"https://docs.googleapis.com/v1/documents/{doc_id}",
                     headers={"Authorization": f"Bearer {tok}"}, timeout=30)
    r.raise_for_status()
    return r.json()["body"]["content"][-1]["endIndex"]


def append(doc_id: str, text: str, title: str = None) -> int:
    tok = _token()
    idx = _end_index(tok, doc_id) - 1  # avant le \n final obligatoire du corps
    prefix = "\n"
    body = prefix + (title + "\n" if title else "") + text.rstrip() + "\n"
    reqs = [{"insertText": {"location": {"index": idx}, "text": body}}]
    if title:
        tstart = idx + len(prefix)
        reqs.append({"updateTextStyle": {
            "range": {"startIndex": tstart, "endIndex": tstart + len(title)},
            "textStyle": {"bold": True, "fontSize": {"magnitude": 13, "unit": "PT"}},
            "fields": "bold,fontSize"}})
    r = requests.post(
        f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
        headers={"Authorization": f"Bearer {tok}"},
        json={"requests": reqs}, timeout=60)
    r.raise_for_status()
    return r.status_code


def main():
    ap = argparse.ArgumentParser(description="Append à la fin d'un Google Doc")
    ap.add_argument("doc_id")
    ap.add_argument("--text-file", required=True, help="fichier texte à ajouter")
    ap.add_argument("--title", help="titre du bloc (mis en gras)")
    args = ap.parse_args()
    text = Path(args.text_file).read_text(encoding="utf-8")
    code = append(args.doc_id, text, args.title)
    print(f"append OK (HTTP {code}) — doc {args.doc_id}")


if __name__ == "__main__":
    main()
