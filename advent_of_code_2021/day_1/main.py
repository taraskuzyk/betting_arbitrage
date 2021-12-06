from pathlib import Path
from typing import List

from definitions import ROOT_DIR
from libs.file_reader import read_file_from_path


def read_int_array_from_file(path: Path) -> List[int]:
    file_text = read_file_from_path(path)
    array_of_strings = file_text.split()
    return [int(string) for string in array_of_strings]


def get_number_of_increases_from_int_array(int_array: List) -> int:
    if len(int_array) in [0, 1]:
        return 0
    int_array_except_first_int = int_array[1:]
    return sum(
        int_array[index] < number
        for index, number in enumerate(int_array_except_first_int)
    )


def get_number_of_increases_from_int_file(path: Path):
    int_array = read_int_array_from_file(path)
    return get_number_of_increases_from_int_array(int_array)


def main():
    path_to_input = ROOT_DIR / "day_1" / "depth_measurements.csv"
    print(f"Number of increases: {get_number_of_increases_from_int_file(path_to_input)}")


if __name__ == "__main__":
    main()
