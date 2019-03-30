class Node:
    def __init__(
            self,
            priority,
            value=None,
            left: 'Node' = None,
            right: 'Node' = None
    ):
        self.priority = priority
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return str(vars(self))

    # for priority queue
    def __lt__(self, other):
        return self.priority < other.priority
