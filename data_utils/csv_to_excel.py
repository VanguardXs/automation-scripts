from __future__ import annotations

from pathlib import Path
import csv
import sys

DEFAULT_DATA_DIR = Path("data")


# ---------- helpers (library-safe) ----------

def unique_path(path: Path) -> Path:
    """If path exists, return path with _1, _2, ..."""
    if not path.exists():
        return path

    parent = path.parent
    stem = path.stem
    suffix = path.suffix

    i = 1
    while True:
        candidate = parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1


def resolve_csv_path(user_input: str) -> Path:
    """Resolve CSV path, also trying DEFAULT_DATA_DIR."""
    p = Path(user_input).expanduser()
    if p.exists():
        return p

    alt = DEFAULT_DATA_DIR / user_input
    if alt.exists():
        return alt

    return p


# ---------- core library function ----------

def csv_to_excel(csv_path: Path, xlsx_path: Path) -> None:
    """
    Convert CSV file to XLSX.
    Raises RuntimeError if openpyxl is missing.
    """
    try:
        import openpyxl
    except ImportError as e:
        raise RuntimeError(
            "openpyxl is required. Install it with: pip install openpyxl"
        ) from e

    wb = openpyxl.Workbook()
    ws = wb.active

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            ws.append(row)

    xlsx_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(xlsx_path)


# ---------- CLI (optional) ----------

def main() -> None:
    if len(sys.argv) >= 2:
        csv_input = sys.argv[1].strip()
    else:
        csv_input = input("Enter path to CSV file: ").strip()

    if not csv_input:
        print("No input provided.")
        return

    csv_path = resolve_csv_path(csv_input)
    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return

    if len(sys.argv) >= 3:
        xlsx_path = Path(sys.argv[2]).expanduser()
    else:
        xlsx_path = csv_path.with_suffix(".xlsx")

    xlsx_path = unique_path(xlsx_path)

    try:
        csv_to_excel(csv_path, xlsx_path)
    except RuntimeError as e:
        print(e)
        return

    print(f"Saved: {xlsx_path}")


if __name__ == "__main__":
    main()
