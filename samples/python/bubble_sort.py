def bubble_sort(nums: list) -> list:
    """
    Classic Bubble Sort.
    Tests nested loops and array mutation.
    """
    n = len(nums)
    for i in range(n):
        for j in range(0, n - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums
