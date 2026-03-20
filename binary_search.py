- """This is a simple binary search implementation."""
+ """Binary search algorithm implementation."""

from typing import List, Optional


def binary_search(nums: List[int], target: int) -> Optional[int]:
    """Search for a target value in a sorted list using binary search.

    Args:
        nums: A sorted list of integers.
        target: The value to search for.

    Returns:
        The index of the target if found, otherwise None.
    """
    if not nums:
        return None

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return None


if __name__ == "__main__":
    sample = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    print(f"List: {sample}")

    for val in [7, 1, 19, 6]:
        result = binary_search(sample, val)
        if result is not None:
            print(f"Found {val} at index {result}")
        else:
            print(f"{val} not found in the list")
