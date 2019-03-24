class Node:
    def __init__(self, priority, value=None, left=None, right=None):
        self._priority = priority

        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return str(vars(self))

    # for priority queue
    def __lt__(self, other):
        return self._priority < other._priority

    @property
    def priority(self):
        return self._priority
