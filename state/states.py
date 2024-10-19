from enum import Enum, auto


class State(Enum):
    music_is_run = auto()
    music_off = auto()
    stop_bot = auto()
