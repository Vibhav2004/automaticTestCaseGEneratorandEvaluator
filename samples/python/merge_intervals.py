def merge_intervals(intervals: list) -> list:
    """
    Given a collection of intervals, merge all overlapping intervals.
    Example Input: [[1,3],[2,6],[8,10],[15,18]]
    Tests 2D array handling and sorting logic.
    """
    if not intervals:
        return []
        
    intervals.sort(key=lambda x: x[0])
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged
