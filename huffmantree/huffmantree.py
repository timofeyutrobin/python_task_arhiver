import queue as q
from .node import Node


class HuffmanTree:
    def __init__(self, wordsFrequencies: dict):
        self._queue = q.PriorityQueue()

        for word in wordsFrequencies:
            priority = wordsFrequencies[word]
            self._queue.put(Node(priority, word))

        while self._queue.qsize() > 1:
            first = self._queue.get()
            second = self._queue.get()

            parentPriority = first.priority + second.priority
            parent = Node(parentPriority, left=first, right=second)
            self._queue.put(parent)

        # last element in queue becomes root
        self._root = self._queue.get()

    @property
    def root(self):
        return self._root
