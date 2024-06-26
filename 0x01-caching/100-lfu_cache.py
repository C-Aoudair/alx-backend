#!/usr/bin/env python3
""" Contains LFUCache class that inherites from BaseCaching.
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """Implement caching system with LFU eviction policy."""

    def __init__(self):
        super().__init__()
        self.key_history = {}

    def put(self, key, item):
        """Add item to self.cache_data dictionary."""
        if not key or not item:
            return

        if key in self.cache_data:
            self.key_history[key] += 1

        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lfu_key = min(self.key_history, key=self.key_history.get)
                print(f"DISCARD: {lfu_key}")
                self.cache_data.pop(lfu_key)
                self.key_history.pop(lfu_key)

            self.cache_data[key] = item
            self.key_history[key] = 1

    def get(self, key):
        """Return the value in self.cache_data linked to key."""
        value = self.cache_data.get(key)
        if value:
            self.key_history[key] += 1
        return value
