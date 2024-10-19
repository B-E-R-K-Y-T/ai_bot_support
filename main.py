import threading

from config import MODEL, BOT_KEYWORD, WAVE_OUTPUT_FILENAME
from parse import recognize_phrase, parse_command
from state.manager import StateManager
from state.states import State
from tools.generate import play_file
from tools.interpreter import run_command
from tools.listen import get_listener


def main():
    listen = get_listener()

    play_file("data/on.wav")

    while True:
        with threading.Lock():
            if StateManager.actual_state is State.stop_bot:
                exit(0)

        listen(2)

        recognized_phrase = recognize_phrase(MODEL, WAVE_OUTPUT_FILENAME)
        print(f"Распознанная фраза: {recognized_phrase}")

        if BOT_KEYWORD in recognized_phrase:
            cmd = parse_command(recognized_phrase)
            print(cmd)

            run_command(cmd)


if __name__ == '__main__':
    main()
