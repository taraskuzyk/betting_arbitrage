from day_1.main import read_int_array_from_file, get_number_of_increases_from_int_array, \
    get_number_of_increases_from_int_file
from definitions import ROOT_DIR

TEST_FILE = ROOT_DIR / "day_1" / "depth_measurements_test.csv"


def test_read_array_from_file():
    some_array = read_int_array_from_file(TEST_FILE)
    assert all(some_array[index] == index + 1 for index in range(3))


def test_get_number_of_increases_from_int_array():
    some_array = [0, 1]
    assert get_number_of_increases_from_int_array(some_array) == 1


def test_get_number_of_increases_with_decreasing_values():
    some_array = [0, -1, -2]
    assert get_number_of_increases_from_int_array(some_array) == 0


def test_get_number_of_increases_with_increasing_and_decreasing_values():
    some_array = [0, 1, 0, 1, 2]
    assert get_number_of_increases_from_int_array(some_array) == 3


def test_get_number_of_increases_from_file():
    """file contents are 1 2 3"""
    assert get_number_of_increases_from_int_file(TEST_FILE) == 2
