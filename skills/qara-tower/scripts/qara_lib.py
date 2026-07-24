"""Config et logique partagée du skill QARA-Tower.

Portable : les chemins sont absolus et ne dépendent PAS de l'emplacement du skill
(le skill existe en double, local projet + global ~/.claude). Les données (JSONL)
vivent à un seul endroit, quel que soit d'où le skill est invoqué.

Rigueur QARA : aucune métrique n'est recalculée ici. On appelle les fonctions de la
Tower (ExploratoryAnalysisService) — la source de vérité de l'application.
"""
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# --- Chemins absolus (portables local/global) --------------------------------
AIMA_TOWER = Path.home() / "Pipeline" / "Aima-Tower"
SRC = AIMA_TOWER / "src"
TRACE_PROD_DB = Path.home() / "Pipeline" / "trace-prod" / "database" / "samples_status.duckdb"
SNAPSHOTS_FILE = AIMA_TOWER / "qara" / "qara_snapshots.jsonl"  # versionné (data/ est gitignored)
GSPREAD_CREDS = Path.home() / ".config" / "gspread" / "authorized_user.json"

# --- Réglages Exis figés (T0) — voir references/metrics-baseline.md -----------
SCORE_SOURCE = "mvaf_v14"       # Exis 1.1
TARGET_SPEC = 0.95             # calibration du seuil de positivité
DORADO = frozenset({"v5.0.0", "v5.2.0"})
MIN_DEPTH = 0.25
EXCLUDE_IND = {"TNE", "Nuclear", "Bladder_Blood", "Bladder_Urine"}
LUNG_EARLY_COHORT = "Lung-DI précoce"


def take_snapshot(timestamp: str = None) -> dict:
    """Mesure l'état courant de la Tower via SES fonctions (aucun recalcul maison).

    Copie trace-prod dans un tmp (évite le lock write du daemon check_samples),
    puis appelle compute() / compute_cohort_cascade() en mode Exis.
    """
    if timestamp is None:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    tmp = Path(tempfile.mkdtemp(prefix="qara_"))
    db = tmp / "snap.duckdb"
    shutil.copy(TRACE_PROD_DB, db)
    os.environ["DUCKDB_PATH"] = str(db)
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    import duckdb
    from exploratory_compute import ExploratoryAnalysisService

    svc = ExploratoryAnalysisService()
    inds = frozenset(i for i in svc.get_indications() if i not in EXCLUDE_IND)

    con = duckdb.connect(str(db), read_only=True)
    tp_total = con.sql("SELECT COUNT(*) FROM samples").fetchone()[0]
    tp_by_type = dict(con.sql(
        "SELECT sample_type, COUNT(*) FROM samples GROUP BY 1").fetchall())
    con.close()

    kw = dict(target_specificity=TARGET_SPEC, indications=inds, min_depth=MIN_DEPTH,
              dorado_version=DORADO, score_source=SCORE_SOURCE)
    r = svc.compute(cohort_mode="advanced", **kw)
    row = r["detection_global"]
    row = row[row["Centre"] == "ALL"].iloc[0]
    st = r["stratified_global"]
    st = st[st["Centre"] == "ALL"].iloc[0]
    re_ = svc.compute(cohort_mode="early", **kw)
    rowe = re_["detection_global"]
    rowe = rowe[rowe["Centre"] == "ALL"].iloc[0]
    casc = svc.compute_cohort_cascade(centre="ALL", cohort_mode="advanced", **kw)

    # Statut par unique_id (post-profondeur), reconstruit avec les briques Tower.
    prep = svc._get_prepared("ALL", "cancer_detection", DORADO, SCORE_SOURCE)
    d = prep[prep["depth"] >= MIN_DEPTH]
    d = d[d["healthy_flag"] | d["indication"].isin(inds)]
    samples = {}
    for t in d.itertuples():
        if t.healthy_flag:
            statut = "sain"
        elif getattr(t, "cohort", None) == LUNG_EARLY_COHORT:
            statut = "precoce"
        elif t.cancer_truth:
            statut = "cancer"
        else:
            statut = "sans_etiquette"
        samples[t.unique_id] = statut

    shutil.rmtree(tmp, ignore_errors=True)

    return {
        "timestamp": timestamp,
        "reglages": {"score": SCORE_SOURCE, "cohorte": "advanced",
                     "specificite_cible": TARGET_SPEC,
                     "dorado": sorted(DORADO), "min_depth": MIN_DEPTH},
        "trace_prod": {"total": tp_total, "par_type": tp_by_type},
        "avances": {
            "seuil": r["threshold"]["ALL"],
            "n_cancer": int(row["N_Cancer"]), "n_healthy": int(row["N_Healthy"]),
            "sensibilite": row["Sens_Cancer_AI"], "specificite": row["Spec_AI"],
            "mut_high": st["Sens_MutHigh"], "mut_low": st["Sens_MutLow"],
            "active_no_mut": st["Sens_Active_NoMut"],
            "par_indication": {x["indication"]: x["Sens_Cancer_AI"]
                               for _, x in r["by_indication_global"].iterrows()},
        },
        "precoce": {"n_cancer": int(rowe["N_Cancer"]),
                    "sensibilite": rowe["Sens_Cancer_AI"]},
        "cascade": [{"name": s["name"], "n": s["n"], "delta": s["delta"]}
                    for s in casc["steps"]],
        "samples": samples,
    }


def load_last_snapshot() -> dict | None:
    """Dernier snapshot enregistré (T_{n-1}), ou None si le journal est vide."""
    if not SNAPSHOTS_FILE.exists():
        return None
    lines = [ln for ln in SNAPSHOTS_FILE.read_text(encoding="utf-8").splitlines()
             if ln.strip()]
    return json.loads(lines[-1]) if lines else None


def persist_snapshot(snap: dict) -> None:
    """Ajoute le snapshot au journal JSONL (append, immuable)."""
    SNAPSHOTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with SNAPSHOTS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(snap, ensure_ascii=False, default=str) + "\n")
