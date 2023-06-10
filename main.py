import sys
from pathlib import Path
import uuid
import shutil

from normalize import normalize

CATEGORIES = {"IMAGE": ['.jpeg', '.png', '.jpg', '.svg'],
              "VIDEO": ['.avi', '.mp4', '.mov', '.mkv'],
              "DOCS": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
              "MUSIC": ['.mp3', '.ogg', '.wav', '.amr'],
              "ARCHIVE": ['.zip', '.gz', '.tar']}


def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        # print(f"Make {target_dir}")
        target_dir.mkdir()
    # print(path.suffix)
    # print(target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}"))
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    if new_name.exists():
        new_name = new_name.with_name(f"{new_name.stem}_{uuid.uuid4()}{file.suffix}")
    file.rename(new_name)


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        # print(item)
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)

    delete_empty_folders(path)
    unpack_archives(path)


def delete_empty_folders(path: Path):
    for item in path.glob("**/*"):
        if item.is_dir() and not any(item.iterdir()):
            item.rmdir()


def unpack_archives(path: Path) -> None:
    archive_dir = path.joinpath("ARCHIVE")
    archive_dir.mkdir(exist_ok=True)
    for item in path.glob("**/*"):
        if item.is_file() and item.suffix.lower() in CATEGORIES["ARCHIVE"]:
            target_dir = archive_dir.joinpath(item.stem)
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.unpack_archive(str(item), str(target_dir))


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return f"Folder with path {path} dos`n exists."

    sort_folder(path)
    # delete_empty_folders(path)
    # upack_archive(path)

    return "All ok"


if __name__ == "__main__":
    print(main())
