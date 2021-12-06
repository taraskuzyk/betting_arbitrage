from definitions import ROOT_DIR
from libs.file_reader import read_file_from_path


def test_read_entire_file():
    text = read_file_from_path(ROOT_DIR / "libs" / "file_reader_test_file.txt")
    assert text == 'xd lol'
