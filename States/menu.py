from .state import State
from app import App
from .button import MenuButton


class Menu(State):
    def __init__(self):
        super().__init__()
        self.buttons = [
            MenuButton((0.5, 0.3), 'PLAY'),
            MenuButton((0.5, 0.5), 'OPTIONS')
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
                if button.text == 'PLAY':
                    self.next = 'game'
                elif button.text == 'OPTIONS':
                    self.next = 'options'

    def draw(self):
        App.window.fill((9, 14, 23))
        for button in self.buttons:
            button.draw()
