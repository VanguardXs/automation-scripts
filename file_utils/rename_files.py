from pathlib import Path
import re


CATEGORY_PREFIX = {
    "image": {"ext": {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}, "prefix": "image_"},
    "video": {"ext": {".mp4", ".mkv", ".mov", ".avi", ".webm"}, "prefix": "video_"},
    "audio": {"ext": {".mp3", ".wav", ".flac", ".aac"}, "prefix": "audio_"},
    "doc": {"ext": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf"}, "prefix": "doc_"},
    "archive": {"ext": {".zip", ".rar", ".7z", ".tar", ".gz"}, "prefix": "archive_"},
}


def safe_name(text: str) -> str:
    text = text.strip().replace(" ", "_")
    text = re.sub(r"[^A-Za-z0-9._-]+", "", text)
    text = re.sub(r"_+", "_", text)
    return text


def detect_prefix_by_ext(file: Path) -> str:
    ext = file.suffix.lower()
    for cfg in CATEGORY_PREFIX.values():
        if ext in cfg["ext"]:
            return cfg["prefix"]
    return "file_"


def unique_path(path: Path) -> Path:
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


def rename_one_file(folder: Path, old_name: str, new_name: str, apply: bool) -> None:
    src = folder / old_name
    if not src.exists() or not src.is_file():
        print(f"File not found: {src}")
        return

    new_name = safe_name(new_name)

    if not new_name:
        prefix = detect_prefix_by_ext(src)  # doc_/image_/file_...
        base = unique_path(folder / f"{prefix}001{src.suffix}")
        target = base
    else:
        if "." not in new_name:
            new_name = new_name + src.suffix
        target = unique_path(folder / new_name)

    print(f"{src.name} -> {target.name}")
    if apply:
        src.rename(target)



def rename_many_files(folder: Path, files: list[Path], prefix_input: str, start_index: int, apply: bool) -> None:
    index = start_index
    for file in files:
        prefix = prefix_input if prefix_input else detect_prefix_by_ext(file)
        new_name = f"{prefix}{index:03d}{file.suffix}"
        target = unique_path(folder / new_name)

        print(f"{file.name} -> {target.name}")
        if apply:
            file.rename(target)

        index += 1


def main() -> None:
    print("=== File Renaming Utility ===")

    folder_input = input("Enter folder path: ").strip()
    folder = Path(folder_input).expanduser()

    if not folder.exists() or not folder.is_dir():
        print("Folder not found.")
        return

    print("\nChoose mode:")
    print("1) Rename ALL files in folder")
    print("2) Rename ONE specific file (by name)")
    print("3) Rename files by extension (e.g. only .jpg)")
    mode = input("Enter 1/2/3: ").strip()

    apply = input("Apply changes? (y/n): ").strip().lower() == "y"
    print("\nMode:", "APPLY" if apply else "PREVIEW (no changes)")
    print("-" * 50)

    if mode == "2":
        old_name = input("Enter exact current filename (e.g. photo.png): ").strip()
        new_name = input("Enter new filename (without path). Extension optional: ").strip()
        rename_one_file(folder, old_name, new_name, apply)
        print("\nDone.")
        return

    # Mode 1 or 3 = batch
    files = sorted([f for f in folder.iterdir() if f.is_file()])

    if mode == "3":
        ext = input("Enter extension (e.g. .jpg or jpg): ").strip().lower()
        if ext and not ext.startswith("."):
            ext = "." + ext
        files = [f for f in files if f.suffix.lower() == ext]

        if not files:
            print("No files with this extension.")
            return

    if mode not in {"1", "3"}:
        print("Invalid mode.")
        return

    prefix_input = input("Enter prefix (Enter = auto): ").strip()
    prefix_input = safe_name(prefix_input)

    try:
        start_index = int(input("Start numbering from (e.g. 1): ").strip())
    except ValueError:
        print("Invalid number.")
        return

    rename_many_files(folder, files, prefix_input, start_index, apply)
    print("\nDone.")


if __name__ == "__main__":
    main()

