#!/usr/bin/env python3
""" Contains LIFOCache class that inherites from BaseCaching.
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Implement caching system with LIFO eviction policy."""

    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """Add item to self.cache_data dictionary."""
        if not key or not item:
            return

        if key in self.cache_data:
            self.cache_data.pop(key)

        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = next(reversed(self.cache_data))
            self.cache_data.pop(last_key)
            print(f"DISCARD: {last_key}")

        self.cache_data[key] = item


    def get(self, key):
        """Return the value in self.cache_data linked to key."""
        return self.cache_data.get(key)
