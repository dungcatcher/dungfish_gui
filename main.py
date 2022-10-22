from app import App
from States.menu import Menu
from States.Game.game import Game
from States.options import Options


def main():
    state_dict = {
        'menu': Menu(),
        'game': Game(),
        'options': Options()
    }
    App.init_states(state_dict, 'menu')
    App.loop()


main()
