from .state import State
from app import App
from util import Button


class Menu(State):
    def __init__(self):
        super().__init__()
        self.buttons = [
            Button((0.5, 0.3), 'PLAY', 'game'),
            Button((0.5, 0.5), 'OPTIONS', 'options')
        ]

    def resize(self):
        for button in self.buttons:
            button.resize()

    def update(self):
        self.draw()
        for button in self.buttons:
            button.update()
            if App.left_click and button.hovered:
                self.done = True
                self.next = button.target_state

    def draw(self):
        App.window.fill((9, 14, 23))
        for button in self.buttons:
            button.draw()
