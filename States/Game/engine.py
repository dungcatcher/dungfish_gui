from subprocess import Popen, PIPE


cmd = r'C:\Users\User\PycharmProjects\dungfish_gui\Assets\dungfish.exe'


class Engine:
    task = Popen(cmd, universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='UTF8', bufsize=1)
    best_move = None


def send_to_engine(command):
    Engine.task.stdin.write(f'{command}\n')
    Engine.task.stdin.flush()


def read_engine_output():
    send_to_engine('isready')
    while True:
        response = Engine.task.stdout.readline()
        if 'bestmove' in response:
            bestmove_response = response.split()
            if bestmove_response[1] != '(none)':
                Engine.best_move = bestmove_response[1]
