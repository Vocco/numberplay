"""
Functions for parallel processing support.
"""
from typing import Any, Callable, Generator, List, Tuple


def collect_result(result_list: List[Any]) -> Callable[[Any], None]:
    """
    Create a callback to collect results from an asynchronous function to a list.

    Parameters
    ----------
    result_list : list
        The list which will be updated upon the completion of an asynchronous function call.

    Returns
    -------
    any -> None
        A side-effect callback which appends the passed input to `result_list`.
    """

    def list_appender(result: Any) -> None:
        result_list.append(result)

    return list_appender


def get_chunk_indices(start: int, end: int, chunks: int) -> Generator[Tuple[int, int], None, None]:
    chunk_size = 1 + (end - start) // chunks
    for _ in range(chunks):
        yield start, min(end + 1, start + chunk_size)
        start += chunk_size
