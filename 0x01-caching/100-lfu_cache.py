#!/usr/bin/env python3
""" Contains LFUCache class that inherites from BaseCaching.
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """Implement caching system with LFU eviction policy."""

    def __init__(self):
        super().__init__()
        self.keys_frequency = {}

    def put(self, key, item):
        """Add item to self.cache_data dictionary."""
        if not key or not item:
            return

        if key in self.cache_data:
            self.cache_data.pop(key)

        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lfu_key = min(self.keys_frequency, key=self.keys_frequency.get)
            print(f"DISCARD: {lfu_key}")
            self.cache_data.pop(lfu_key)
            self.keys_frequency.pop(lfu_key)

        self.cache_data[key] = item
        if key not in self.keys_frequency:
            self.keys_frequency[key] = 1
        else:
            self.keys_frequency[key] += 1

    def get(self, key):
        """Return the value in self.cache_data linked to key."""
        value = self.cache_data.get(key)
        if value:
            self.keys_frequency[key] += 1
        return value
