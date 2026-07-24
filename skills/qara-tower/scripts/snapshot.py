"""Capture un snapshot T_n de l'état de la Tower (mode Exis).

Usage :
    python snapshot.py                 # affiche le snapshot JSON sur stdout
    python snapshot.py --out T_n.json  # écrit dans un fichier
    python snapshot.py --persist       # ajoute au journal qara/qara_snapshots.jsonl
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qara_lib  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Snapshot QARA de la Tower")
    ap.add_argument("--persist", action="store_true",
                    help="mesure puis ajoute le snapshot au journal JSONL")
    ap.add_argument("--out", help="écrit le snapshot dans ce fichier (sinon stdout)")
    ap.add_argument("--persist-file",
                    help="persiste un snapshot DÉJÀ mesuré (JSON) sans re-mesurer "
                         "— garantit que le point journalisé == le point comparé")
    args = ap.parse_args()

    # Persistance d'un snapshot déjà pris (rigueur : même point comparé et journalisé)
    if args.persist_file:
        snap = json.loads(Path(args.persist_file).read_text(encoding="utf-8"))
        qara_lib.persist_snapshot(snap)
        print(f"[persisté depuis {args.persist_file} dans {qara_lib.SNAPSHOTS_FILE}]",
              file=sys.stderr)
        return

    snap = qara_lib.take_snapshot()
    js = json.dumps(snap, ensure_ascii=False, default=str, indent=2)
    if args.out:
        Path(args.out).write_text(js, encoding="utf-8")
        print(f"snapshot écrit dans {args.out}", file=sys.stderr)
    else:
        print(js)

    if args.persist:
        qara_lib.persist_snapshot(snap)
        print(f"[persisté dans {qara_lib.SNAPSHOTS_FILE}]", file=sys.stderr)


if __name__ == "__main__":
    main()
