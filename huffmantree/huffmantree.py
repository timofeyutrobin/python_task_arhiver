import queue as q
from .node import Node


class HuffmanTree:
    def __init__(self, words_probabilities: dict):
        self._codes = {}
        self._queue = q.PriorityQueue()

        for word in words_probabilities:
            priority = words_probabilities[word]
            self._queue.put(Node(priority, word))

        while self._queue.qsize() > 1:
            first = self._queue.get()
            second = self._queue.get()

            parent_priority = first.priority + second.priority
            parent = Node(parent_priority, left=first, right=second)
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

    def _get_codes(self, root, current_code: str):
        if root is None:
            return
        if root.value:
            self._codes[root.value] = current_code
            return
        self._get_codes(root.left, current_code + '0')
        self._get_codes(root.right, current_code + '1')
