from typing import Tuple


def offset_range(
    current_range: Tuple[int, int],
    inserted_range: Tuple[int, int],
    offset: int,
) -> Tuple[int, int]:
    """Update current range based on inserted range and previous range.

    Args:
        current_range: The range you wish the indices to be updated for.
        inserted_range: The range of the inserted range.
        offset: The offset to apply to the current range.
    """

    start, end = current_range

    if offset == 0:
        return current_range

    is_within_range = (
        inserted_range[0] <= start <= inserted_range[1]
        or inserted_range[0] <= end <= inserted_range[1]
    )
    if is_within_range:
        return start, end + offset

    is_before_range = start < inserted_range[0]
    if is_before_range:
        return start, end

    is_after_range = end > inserted_range[1]
    if is_after_range:
        return start + offset, end + offset

    raise ValueError(
        f"Current range {current_range} is not within inserted range {inserted_range}",
    )
