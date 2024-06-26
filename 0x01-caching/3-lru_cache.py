#!/usr/bin/env python3
""" Contains LRUCache class that inherites from BaseCaching.
"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """Implement caching system with LRU eviction policy."""

    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """Add item to self.cache_data dictionary."""
        if not key or not item:
            return

        if key in self.cache_data:
            self.cache_data.pop(key)

        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            first_key = next(iter(self.cache_data))
            print(f"DISCARD: {first_key}")
            self.cache_data.pop(first_key)

        self.cache_data[key] = item

    def get(self, key):
        """Return the value in self.cache_data linked to key."""
        value = self.cache_data.pop(key, None)
        if value is not None:
            self.cache_data[key] = value
        return value
