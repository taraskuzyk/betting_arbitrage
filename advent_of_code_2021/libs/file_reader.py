from pathlib import Path


def read_file_from_path(path: Path):
    with open(path) as file:
        return file.read()

