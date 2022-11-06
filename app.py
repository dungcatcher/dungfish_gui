import pygame
import pygame_widgets


class App:
    pygame.init()
    pygame.mixer.init()

    pygame.display.set_caption('Dungfish ILP project')

    window = pygame.display.set_mode((960, 590), pygame.RESIZABLE)
    HIGH_RES = (1920, 1080)

    _done = False
    _state_dict = None
    _current_state = None
    _clock = pygame.time.Clock()

    left_click = False
    events = None
    dt = 0

    @staticmethod
    def init_states(state_dict, start_state_name):
        App._state_dict = state_dict
        App._current_state = App._state_dict[start_state_name]

    @staticmethod
    def flip_state():
        App._current_state.done = False
        App._current_state = App._state_dict[App._current_state.next]

    @staticmethod
    def update():
        if App._current_state.done:
            App.flip_state()
        pygame_widgets.update(App.events)
        App._current_state.update()

    @staticmethod
    def event_loop():
        App.left_click = False
        App.events = pygame.event.get()
        for event in App.events:
            if event.type == pygame.QUIT:
                App._done = True
            if event.type == pygame.VIDEORESIZE:
                for state in App._state_dict.values():
                    state.resize()
            if event.type == pygame.MOUSEBUTTONDOWN:
                App.left_click = True

    @staticmethod
    def close():
        for state in App._state_dict.values():
            state.close()

    @staticmethod
    def loop():
        while not App._done:
            try:
                App.dt = App._clock.tick(60) / 1000

                App.event_loop()
                App.update()

                pygame.display.update()
            except KeyboardInterrupt:  # Handle Ctrl+c
                App._done = True

        App.close()
        pygame.quit()
