#!/usr/bin/env python3
"""
This module contains a simple pagination with hypermedia inplementation
"""
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """
    eturn a tuple of size two containing a start index and an end index
    """

    startIndex = (page - 1) * page_size
    endIndex = startIndex + page_size

    return (startIndex, endIndex)


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Takes two arguments and return the appropriate page of
        the dataset.
        """
        assert type(page) is int and type(page_size) is int
        assert page > 0 and page_size > 0

        indexes = index_range(page, page_size)

        try:
            start, end = indexes
            pages = self.dataset()
            data = pages[start:end]
        except IndexError:
            data = []

        return data

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """akes two arguments and return the appropriate page of
        the dataset with hypermedia links.
        """
        numberOfPages = math.ceil(len(self.dataset()) / page_size)

        data = self.get_page(page, page_size)
        previousPage = page - 1 if page > 1 else None
        nextPage = page + 1 if page < numberOfPages else None

        return {
            "page_size": page_size,
            "page": page,
            "data": data,
            "next_page": nextPage,
            "prev_page": previousPage,
            "total_pages": numberOfPages,
        }
