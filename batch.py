class Batch:
    """
    Calls flush_function and resets the data buffer
    whenever capacity is reached.
    """
    def __init__(self, capacity, flush_function):
        self.data = []
        self.flush_function = flush_function
        self.capacity = capacity

    def add(self, item):
        self.data.append(item)
        if len(self.data) == self.capacity:
            self.flush()
            self.reset()

    def reset(self):
        self.data = []

    def flush(self):
        self.flush_function(self.data)
        self.data = []
