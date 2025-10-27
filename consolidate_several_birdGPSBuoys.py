#!/usr/bin/env python3
# file: tools/qaanaaq_consolidate_final_strict.py
"""
Create a NEW workbook based on your provided template:
- Keeps all existing 2022/2023 sheets from All_birds_all_points.xlsx.
- Adds new per-bird sheets for 2024 and 2025 populated from the specified files.
- Detects data in sheet 'Reports' (as seen in Havoern_2022-2025.xlsx).
- Never overwrites the original; writes All_birds_all_points_CONSOLIDATED.xlsx (auto-suffixed if needed).
"""

from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd

# ---- Fixed paths (yours) -----------------------------------------------------
TEMPLATE_PATH = Path("DATA/All_birds_all_points.xlsx")  # provided template
INPUT_FILES = [
    Path("/dmidata/archive/arch1/home/ang/qaanaaq_fielddata/2025-2022_Trusted_GPStracker/Mallemuk_2022-2024.xlsx"),
    Path("/dmidata/archive/arch1/home/ang/qaanaaq_fielddata/2025-2022_Trusted_GPStracker/Soekonge_2022-2025.xlsx"),
    Path("/dmidata/archive/arch1/home/ang/qaanaaq_fielddata/2025-2022_Trusted_GPStracker/Ismaage_2022-2025.xlsx"),
    Path("/dmidata/archive/arch1/home/ang/qaanaaq_fielddata/2025-2022_Trusted_GPStracker/Edder_2022-2025.xlsx"),
    Path("/dmidata/archive/arch1/home/ang/qaanaaq_fielddata/2025-2022_Trusted_GPStracker/Havoern_2022-2025.xlsx"),
    Path("/dmidata/archive/arch1/home/ang/qaanaaq_fielddata/2025-2022_Trusted_GPStracker/Havterne_2022-2025.xlsx"),
]
# Also accept the attached demo path if running locally:
LOCAL_OVERRIDE = Path("fejl/Havoern_2022-2025.xlsx")
if LOCAL_OVERRIDE.exists() and all(p.name != LOCAL_OVERRIDE.name for p in INPUT_FILES):
    INPUT_FILES.append(LOCAL_OVERRIDE)

PREFERRED_OUTPUT = Path("OUTPUT/All_birds_all_points_CONSOLIDATED.xlsx")
# -----------------------------------------------------------------------------

TARGET_YEARS = {2024, 2025}

# Primary timestamp candidates found in real files (incl. your attached example)
TIMESTAMP_CANDIDATES: List[str] = [
    "Timestamp UTC", "Timestamp_UTC", "timestamp_utc",
    "datetime", "date_time", "time", "timestamp",
]

# Normalize names (spaces/underscores/case/units removed)
def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.strip().lower())

# Build a normalization-based mapper + a few explicit pairs
def map_columns_to_template(df: pd.DataFrame, template_cols: List[str]) -> pd.DataFrame:
    norm_in = { _norm(c): c for c in df.columns }
    mapped = {}
    for tc in template_cols:
        n = _norm(tc)
        if n in norm_in:
            mapped[norm_in[n]] = tc
    # Extra explicit mappings commonly seen in the “Reports” sheet
    explicit = {
        "Timestamp UTC": "Timestamp_UTC",
        "Unit ActivationDate UTC": "Unit_ActivationDate_UTC",
        "GPS Speed(Km/h)": "GPS_Speed_Km_h_",
        "GPS Altitude(m)": "GPS_Altitude_m_",
        "Accuracy(m)": "Accuracy_m_",
        "Temperature(°C)": "Temperature__C_",
        "Temperature Min(°C)": "TemperatureMin__C_",
        "Temperature Max(°C)": "TemperatureMax__C_",
        "Group": "Group_",
    }
    for src, dst in explicit.items():
        if src in df.columns and dst in template_cols:
            mapped[src] = dst

    out = df.rename(columns=mapped).copy()
    for col in template_cols:
        if col not in out.columns:
            out[col] = pd.NA
    # Final ordering: template columns only (trace columns added later when writing if needed)
    return out[template_cols]

def safe_output_path(preferred: Path) -> Path:
    if not preferred.exists():
        return preferred
    i = 2
    while True:
        cand = preferred.with_name(f"{preferred.stem}_v{i}{preferred.suffix}")
        if not cand.exists():
            return cand
        i += 1

def template_columns_and_sheets(template_path: Path) -> Tuple[List[str], List[str]]:
    xls = pd.ExcelFile(template_path)
    sheets = xls.sheet_names[:]
    first = sheets[0]
    cols = list(pd.read_excel(template_path, sheet_name=first, nrows=0).columns)
    if not cols:
        raise ValueError("Template has no columns.")
    return cols, sheets

def bird_from_filename(path: Path) -> str:
    m = re.match(r"([A-Za-zÆØÅæøå]+)_", path.stem)
    return m.group(1) if m else path.stem

def timestamp_column(df: pd.DataFrame) -> Optional[str]:
    low = {c.lower(): c for c in df.columns}
    for cand in TIMESTAMP_CANDIDATES:
        if cand in df.columns:
            return cand
        if cand.lower() in low:
            return low[cand.lower()]
    return None

def read_reports_or_all(path: Path) -> pd.DataFrame:
    # Prefer sheet named 'Reports'; else read all sheets
    xls = pd.ExcelFile(path)
    if "Reports" in xls.sheet_names:
        df = pd.read_excel(path, sheet_name="Reports")
        return df
    frames = []
    for sh in xls.sheet_names:
        try:
            df = pd.read_excel(path, sheet_name=sh)
            if df is not None and not df.empty:
                frames.append(df)
        except Exception:
            continue
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def build_for_years(df: pd.DataFrame, bird: str, template_cols: List[str]) -> Dict[int, pd.DataFrame]:
    if df is None or df.empty:
        return {}
    # Ensure UnitName populated
    if "UnitName" not in df.columns or df["UnitName"].isna().all():
        df["UnitName"] = bird
    # Find/parse timestamp
    tcol = timestamp_column(df)
    if tcol is None:
        return {}
    df[tcol] = pd.to_datetime(df[tcol], errors="coerce", utc=False)
    df = df[df[tcol].notna()].copy()
    if df.empty:
        return {}
    df["__Year__"] = df[tcol].dt.year

    out: Dict[int, pd.DataFrame] = {}
    for y in TARGET_YEARS:
        part = df[df["__Year__"] == y].copy()
        if part.empty:
            continue
        # Align to template schema/order
        if tcol != "Timestamp_UTC" and "Timestamp_UTC" in template_cols:
            part = part.rename(columns={tcol: "Timestamp_UTC"})
        part = map_columns_to_template(part, template_cols)
        if "Timestamp_UTC" in part.columns:
            part = part.sort_values(["UnitName", "Timestamp_UTC"]).reset_index(drop=True)
        out[y] = part
    return out

def run() -> Path:
    template_cols, template_sheet_names = template_columns_and_sheets(TEMPLATE_PATH)
    per_bird_year: Dict[Tuple[str, int], pd.DataFrame] = {}
    summary: List[Dict[str, object]] = []

    for fpath in INPUT_FILES:
        if not fpath.exists():
            summary.append({"Bird": bird_from_filename(fpath), "Year": None, "Rows": 0, "File": str(fpath), "Note": "missing"})
            continue
        bird = bird_from_filename(fpath)
        raw = read_reports_or_all(fpath)
        parts = build_for_years(raw, bird, template_cols)
        for year, frame in parts.items():
            key = (bird, year)
            per_bird_year[key] = pd.concat([per_bird_year.get(key, pd.DataFrame()), frame], ignore_index=True)
            summary.append({"Bird": bird, "Year": year, "Rows": len(frame), "File": fpath.name})

    output_path = safe_output_path(PREFERRED_OUTPUT)

    with pd.ExcelWriter(output_path, engine="openpyxl", mode="w") as writer:
        # Copy original tabs (e.g., all 2022/2023)
        txls = pd.ExcelFile(TEMPLATE_PATH)
        for sh in txls.sheet_names:
            tdf = pd.read_excel(TEMPLATE_PATH, sheet_name=sh)
            tdf.to_excel(writer, sheet_name=sh, index=False)

        # Write NEW tabs (2024/2025) with real rows
        wrote_any = False
        for (bird, year), frame in sorted(per_bird_year.items()):
            if frame.empty:
                continue
            frame.to_excel(writer, sheet_name=f"{bird}{year}", index=False)
            wrote_any = True

        # Small sanity summary
        if summary:
            pd.DataFrame(summary).sort_values(["Bird", "Year"]).to_excel(
                writer, sheet_name="_Summary_2024_2025", index=False
            )

    print(f"[OK] New workbook created: {output_path}")
    if not wrote_any:
        print("[WARN] No 2024/2025 tabs were created. Check 'Timestamp UTC' exists/has data in the inputs.")
    return output_path

if __name__ == "__main__":
    run()

