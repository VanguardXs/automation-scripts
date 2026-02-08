from __future__ import annotations

from pathlib import Path
import csv
import sys

try:
    import openpyxl
except ImportError:
    print("openpyxl is required. Install it with: pip install openpyxl")
    sys.exit(1)


DEFAULT_DATA_DIR = Path("data")


def unique_path(path: Path) -> Path:
    """
    If 'path' exists, return a new path like name_1.xlsx, name_2.xlsx, ...
    """
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
    """
    Resolve CSV path.
    - If user provided a valid existing path -> use it
    - Else try DEFAULT_DATA_DIR / user_input (e.g. data/file.csv)
    """
    p = Path(user_input).expanduser()

    if p.exists():
        return p

    alt = DEFAULT_DATA_DIR / user_input
    if alt.exists():
        return alt

    return p  # return original (for correct 'File not found' message)


def csv_to_excel(csv_path: Path, xlsx_path: Path) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            ws.append(row)

    wb.save(xlsx_path)


def main() -> None:
    # Input CSV: argv[1] or prompt
    if len(sys.argv) >= 2:
        csv_input = sys.argv[1].strip()
    else:
        csv_input = input("Enter path to CSV file: ").strip()

    if not csv_input:
        print("No input provided. Exit.")
        return

    csv_path = resolve_csv_path(csv_input)

    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        print("Tip: try 'data/your_file.csv' if your CSV is inside the data folder.")
        return

    # Output XLSX: argv[2]
    if len(sys.argv) >= 3:
        xlsx_path = Path(sys.argv[2]).expanduser()
    else:
        xlsx_path = csv_path.with_suffix(".xlsx")

    # Avoid overwriting: auto create unique filename
    xlsx_path = unique_path(xlsx_path)

    csv_to_excel(csv_path, xlsx_path)
    print(f"Saved: {xlsx_path}")


if __name__ == "__main__":
    main()
