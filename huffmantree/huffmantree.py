import queue as q
from .node import Node


class HuffmanTree:
    def __init__(self, bytes_probabilities: dict):
        self._codes = {}
        self._queue = q.PriorityQueue()
        self._nodes_count = 1

        if len(bytes_probabilities) == 1:
            for word in bytes_probabilities:
                priority = bytes_probabilities[word]
                self._root = Node(priority, )
                self._codes = {word: '0'}
        else:
            for word in bytes_probabilities:
                priority = bytes_probabilities[word]
                self._queue.put(Node(priority, word))

            while self._queue.qsize() > 1:
                first = self._queue.get()
                second = self._queue.get()

                parent_priority = first.priority + second.priority
                parent = Node(parent_priority, left=first, right=second)
                self._queue.put(parent)
                self._nodes_count += 2

            self._root = self._queue.get()
            self._get_codes(self._root, '')

        self._head = self._root

    @property
    def root(self):
        return self._root

    @property
    def codes(self):
        return self._codes

    def get_code(self, byte):
        return self._codes[byte]

    def search(self, bit):
        if bit == 0:
            self._head = self._head.left
        elif bit == 1:
            self._head = self._head.right
        else:
            raise AttributeError('Bit must be 1 or 0')
        value = self._head.value
        if value is not None:
            self._head = self._root
            return value

    def _get_codes(self, root, current_code: str):
        if root is None:
            return
        if root.value is not None:
            self._codes[root.value] = current_code
            return
        self._get_codes(root.left, current_code + '0')
        self._get_codes(root.right, current_code + '1')
