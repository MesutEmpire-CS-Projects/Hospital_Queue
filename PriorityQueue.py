from datetime import datetime


class PriorityQueueBase:
    """Abstract base class for a priority queue."""

    class _Item:
        """Lightweight composite to store priority queue items."""
        __slots__ = '_key', '_value', '_index', '_time_added'

        def __init__(self, k, v):
            self._key = k
            self._value = v
            self._index = None  # Updated during insertion
            self._time_added = datetime.now()

        def __lt__(self, other):
            # Compare based on priority and then on the time added
            if self._key == other._key:
                return self._time_added < other._time_added
            return self._key < other._key

    def is_empty(self):  # concrete method assuming abstract len
        """Return True if the priority queue is empty."""
        return len(self) == 0


class Empty(Exception):
    def __init__(self, message="The container is empty."):
        self.message = message
        super().__init__(self.message)
