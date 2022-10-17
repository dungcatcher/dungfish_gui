import pygame


class App:
    pygame.init()
    pygame.display.set_caption('Dungfish ILP project')

    window = pygame.display.set_mode((960, 590), pygame.RESIZABLE)
    HIGH_RES = (1920, 1080)

    _done = False
    _state_dict = None
    _current_state = None

    left_click = False

    @staticmethod
    def init_states(state_dict, start_state_name):
        App._state_dict = state_dict
        App._current_state = App._state_dict[start_state_name]

    @staticmethod
    def flip_state():
        App._current_state = App._state_dict[App._current_state.next]

    @staticmethod
    def update():
        if App._current_state.done:
            App.flip_state()
        App._current_state.update()

    @staticmethod
    def event_loop():
        App.left_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                App._done = True
            if event.type == pygame.VIDEORESIZE:
                for state in App._state_dict.values():
                    state.resize()
            if event.type == pygame.MOUSEBUTTONDOWN:
                App.left_click = True

    @staticmethod
    def loop():
        while not App._done:
            App.event_loop()
            App.update()

            pygame.display.update()

        pygame.quit()
