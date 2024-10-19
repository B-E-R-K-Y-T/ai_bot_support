import random
import threading
from datetime import datetime
from decimal import Decimal

from state.context import Context
from state.manager import StateManager
from state.states import State
from tools.generate import play_file, say
from tools.util import sound_signal


def play_music_do():
    with threading.Lock():
        StateManager.actual_state = State.music_is_run

    play_file("data/Baroque Harpsichord and Strings 30.wav")


@sound_signal
def add_volume_do():
    with threading.Lock():
        if Context.volume <= Decimal("0.9"):
            Context.volume += Decimal("0.1")
        elif Context.volume >= Decimal("0.9"):
            Context.volume = Decimal("0.0")


@sound_signal
def sub_volume_do():
    with threading.Lock():
        if Context.volume >= Decimal("0.1"):
            Context.volume -= Decimal("0.1")
        elif Context.volume <= Decimal("0.1"):
            Context.volume = Decimal("0.0")


def what_volume_do():
    with threading.Lock():
        say(f"текущий уровень громкости: {Context.volume}")


def what_time_do():
    current_time = datetime.now().strftime("%H:%M")
    say(current_time)


def hello_do():
    phrases = (
        "Привет, человек!",
        "Привет",
        "Здрасте",
        "Велком!",
        "Здравствуйте",
        "Привет, программист",
        "Прив",
        "Приветик",
        "Приветос",
        "Какой хороший день! Привет-привет!",
        "Привет-привет!",
    )

    say(random.choice(phrases))


def stop_do():
    with threading.Lock():
        if StateManager.actual_state is State.music_is_run:
            say("Выключаю музыку")

            StateManager.actual_state = State.music_off
        else:
            say("Пока!")

            play_file("data/off.wav")

            StateManager.actual_state = State.stop_bot


def default_do():
    say("Я вас не понимаю, попробуйте спросить иначе")
