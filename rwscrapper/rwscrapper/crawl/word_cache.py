# -*- coding: utf-8 -*-

import time
import random

class WordCache(object):
    """
    Denote a LRU word cache
    """
    def __init__(self, max_capacity):
        self._max_capacity = max_capacity
        self._cache = {}

    def __str__(self):
        return str(self._cache)

    def __len__(self):
        return len(self._cache)

    def find(self, word):
        """
        Search a word in cache
        """
        return word in self._cache

    def add(self, word):
        """
        If there is enough room add a new word in cache,
        Otherwise select the oldest and replace it
        """
        if len(self._cache) < self._max_capacity:
            self._cache[word] = time.time()
        else:
            oldest = min(self._cache.items(), key = lambda x : x[1])[0]
            del self._cache[oldest]
            self._cache[word] = time.time()


if __name__ == "__main__":
        wc = WordCache(5)
        wlist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        for i in range(1000):
            word = random.choice(wlist)
            if not wc.find(word):
                wc.add(word)
