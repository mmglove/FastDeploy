"""Unit tests for the binary_search module."""

import sys
from pathlib import Path

import pytest

# Import directly from the root-level script
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from binary_search import binary_search


def test_target_found_in_middle():
    assert binary_search([1, 3, 5, 7, 9], 5) == 2


def test_target_found_at_start():
    assert binary_search([1, 3, 5, 7, 9], 1) == 0


def test_target_found_at_end():
    assert binary_search([1, 3, 5, 7, 9], 9) == 4


def test_target_not_found():
    assert binary_search([1, 3, 5, 7, 9], 4) is None


def test_empty_list():
    assert binary_search([], 1) is None


def test_single_element_found():
    assert binary_search([42], 42) == 0


def test_single_element_not_found():
    assert binary_search([42], 7) is None


def test_two_elements_first():
    assert binary_search([2, 4], 2) == 0


def test_two_elements_second():
    assert binary_search([2, 4], 4) == 1


def test_large_list():
    nums = list(range(0, 200, 2))  # [0, 2, 4, ..., 198]
    assert binary_search(nums, 100) == 50
    assert binary_search(nums, 101) is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
