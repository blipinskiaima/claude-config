"""Compare l'état courant T_n au dernier snapshot enregistré T_{n-1}.

Sortie : un diff JSON (deltas agrégés + entrants/sortants/changements nommés).
Si aucun snapshot antérieur n'existe, renvoie le résumé de T0 (baseline).

Usage :
    python compare.py                       # mesure T_n maintenant, compare au dernier
    python compare.py --current T_n.json    # utilise un snapshot déjà pris
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qara_lib  # noqa: E402


def _summary(snap: dict) -> dict:
    a = snap["avances"]
    return {
        "trace_prod_total": snap["trace_prod"]["total"],
        "n_cancer": a["n_cancer"], "n_healthy": a["n_healthy"],
        "seuil": a["seuil"], "sensibilite": a["sensibilite"],
        "specificite": a["specificite"],
    }


def build_diff(prev: dict, cur: dict) -> dict:
    d = {"de": prev["timestamp"] if prev else None, "a": cur["timestamp"],
         "est_baseline": prev is None}
    if prev is None:
        d["note"] = "T0 — point de référence initial, aucune comparaison."
        d["baseline"] = _summary(cur)
        return d

    pa, ca = prev["avances"], cur["avances"]
    d["trace_prod"] = _delta(prev["trace_prod"]["total"], cur["trace_prod"]["total"])
    d["cohorte_cancer"] = _delta(pa["n_cancer"], ca["n_cancer"])
    d["cohorte_healthy"] = _delta(pa["n_healthy"], ca["n_healthy"])
    d["seuil"] = {"avant": pa["seuil"], "apres": ca["seuil"],
                  "identique": pa["seuil"] == ca["seuil"]}
    d["sensibilite"] = {"avant": pa["sensibilite"], "apres": ca["sensibilite"]}
    d["specificite"] = {"avant": pa["specificite"], "apres": ca["specificite"]}
    d["par_indication"] = {
        ind: {"avant": pa["par_indication"].get(ind), "apres": v}
        for ind, v in ca["par_indication"].items()
        if pa["par_indication"].get(ind) != v
    }

    ps, cs = prev.get("samples", {}), cur.get("samples", {})
    entrants = {u: cs[u] for u in cs if u not in ps}
    sortants = {u: ps[u] for u in ps if u not in cs}
    changements = {u: {"avant": ps[u], "apres": cs[u]}
                   for u in cs if u in ps and ps[u] != cs[u]}
    d["samples"] = {
        "n_entrants": len(entrants), "n_sortants": len(sortants),
        "n_changements": len(changements),
        "entrants": entrants, "sortants": sortants, "changements_statut": changements,
    }
    return d


def _delta(avant, apres):
    return {"avant": avant, "apres": apres, "delta": apres - avant}


def main():
    ap = argparse.ArgumentParser(description="Diff QARA T_n vs T_{n-1}")
    ap.add_argument("--current", help="fichier snapshot T_n (sinon on mesure maintenant)")
    args = ap.parse_args()

    if args.current:
        cur = json.loads(Path(args.current).read_text(encoding="utf-8"))
    else:
        cur = qara_lib.take_snapshot()
    prev = qara_lib.load_last_snapshot()
    print(json.dumps(build_diff(prev, cur), ensure_ascii=False, default=str, indent=2))


if __name__ == "__main__":
    main()
