def two_sum(nums: list, target: int) -> list:
    """
    Find two indices that sum up to target.
    Tests dictionary (hash map) usage and list returns.
    """
    prevMap = {} # val : index
    for i, n in enumerate(nums):
        diff = target - n
        if diff in prevMap:
            return [prevMap[diff], i]
        prevMap[n] = i
    return []
