from __future__ import annotations

from pathlib import Path
import csv
import re

from data_utils.csv_to_excel import csv_to_excel, unique_path

DEFAULT_DATA_DIR = Path("data")


def normalize_space(s: str) -> str:
    s = s.replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            rows.append({k: (v if v is not None else "") for k, v in r.items()})
        return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    headers = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)


def strip_all(rows: list[dict]) -> list[dict]:
    return [{k: normalize_space(str(v)) for k, v in r.items()} for r in rows]


def drop_empty_rows(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        if any(normalize_space(str(v)) for v in r.values()):
            out.append(r)
    return out


def select_columns(rows: list[dict], columns: list[str]) -> list[dict]:
    cols = [c for c in columns if c]
    return [{c: r.get(c, "") for c in cols} for r in rows]


def drop_duplicates(rows: list[dict], key_cols: list[str] | None) -> list[dict]:
    if not rows:
        return rows

    cols = key_cols if key_cols else list(rows[0].keys())

    seen = set()
    out = []
    for r in rows:
        key = tuple(r.get(c, "") for c in cols)
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def resolve_input_path(user_input: str) -> Path:
    p = Path(user_input).expanduser()
    if p.exists():
        return p
    return DEFAULT_DATA_DIR / user_input


def main() -> None:
    print("=== CSV Cleaner ===")

    csv_in_raw = input("Enter path to CSV (e.g. data/file.csv): ").strip()
    if not csv_in_raw:
        print("No input provided.")
        return

    csv_path = resolve_input_path(csv_in_raw)
    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return

    rows = read_csv(csv_path)
    if not rows:
        print("CSV is empty.")
        return

    print("\nChoose actions (y/n):")
    do_strip = input("1) Trim/normalize spaces in all cells? (y/n): ").strip().lower() == "y"
    do_drop_empty = input("2) Remove empty rows? (y/n): ").strip().lower() == "y"
    do_select_cols = input("3) Keep only specific columns? (y/n): ").strip().lower() == "y"
    do_dedupe = input("4) Remove duplicates? (y/n): ").strip().lower() == "y"

    if do_strip:
        rows = strip_all(rows)

    if do_drop_empty:
        rows = drop_empty_rows(rows)

    if do_select_cols:
        print("\nAvailable columns:")
        print(", ".join(rows[0].keys()))
        cols_raw = input("Enter columns separated by comma: ").strip()
        cols = [c.strip() for c in cols_raw.split(",")] if cols_raw else []
        if cols:
            rows = select_columns(rows, cols)

    if do_dedupe:
        use_keys = input("Use specific key columns for duplicates? (y/n): ").strip().lower() == "y"
        keys = None
        if use_keys:
            print("\nAvailable columns:")
            print(", ".join(rows[0].keys()))
            keys_raw = input("Enter key columns separated by comma: ").strip()
            keys = [k.strip() for k in keys_raw.split(",")] if keys_raw else None
        rows = drop_duplicates(rows, keys)

    out_path = csv_path.parent / f"cleaned_{csv_path.stem}.csv"
    write_csv(out_path, rows)
    print(f"\nSaved CSV: {out_path}")

    to_xlsx = input("Also export to XLSX? (y/n): ").strip().lower() == "y"
    if to_xlsx:
        xlsx_path = unique_path(out_path.with_suffix(".xlsx"))
        try:
            csv_to_excel(out_path, xlsx_path)
            print(f"Saved XLSX: {xlsx_path}")
        except RuntimeError as e:
            print(e)


if __name__ == "__main__":
    main()
