class State:
    def __init__(self):
        super().__init__()
        self.done = False
        self.next = None

    def resize(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def change_state(self, state):
        self.next = state
        self.done = True
