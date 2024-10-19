import functools
from typing import Callable

from tools.generate import play_file


def sound_signal(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        play_file("data/something_do.wav")

        return func(*args, **kwargs)

    return wrapper
