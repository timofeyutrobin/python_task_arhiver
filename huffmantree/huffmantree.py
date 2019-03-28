import queue as q
from .node import Node


class HuffmanTree:
    def __init__(self, wordsFrequencies: dict):
        self._codes = {}
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

        self._get_codes(self._root, '')

    @property
    def root(self):
        return self._root

    @property
    def codes(self):
        return self._codes

    def _get_codes(self, root, currentCode: str):
        if root is None:
            return
        if root.value:
            self._codes[root.value] = currentCode
            return
        self._get_codes(root.left, currentCode + '0')
        self._get_codes(root.right, currentCode + '1')
