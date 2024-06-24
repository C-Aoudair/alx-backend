#!/use/bin/env python3
"""
This module contains index_range function.
"""


def index_range(page: int, page_size: int) -> tuple:
    """
    eturn a tuple of size two containing a start index and an end index
    """

    startIndex = (page - 1) * page_size
    endIndex = startIndex + page_size

    return (startIndex, endIndex)
