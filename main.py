from app import App
from States.menu import Menu
from States.Game.game import Game


def main():
    state_dict = {
        'menu': Menu(),
        'game': Game()
    }
    App.init_states(state_dict, 'menu')
    App.loop()


main()
