from States.state import State
from app import App


class Game(State):
    def __init__(self):
        super().__init__()

    def update(self):
        self.draw()

    def draw(self):
        App.window.fill((0, 0, 0))
        