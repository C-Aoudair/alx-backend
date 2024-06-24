#!/usr/bin/env python3
"""
This module contains a simple pagination inplementation
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
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
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
            page = pages[start: end]
        except IndexError:
            page = []

        return page
