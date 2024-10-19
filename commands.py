import threading
from typing import Callable

from executers import (
    play_music_do,
    what_time_do,
    hello_do,
    default_do,
    stop_do,
    add_volume_do,
    sub_volume_do,
    what_volume_do
)


class Command:
    def __init__(self, text: str, runner: Callable):
        self.text = text
        self.__command = [token for token in self.text.split(" ") if token]
        self.__runner = runner

    @property
    def command(self):
        return self.__command

    def execute(self):
        t = threading.Thread(
            target=self.__runner
        )

        t.daemon = True
        t.start()


class ManagerCommand:
    DEFAULT_DO = Command("_", default_do)

    @classmethod
    def get_commands(cls):
        commands = []

        for name_attr in dir(cls):
            attr = getattr(cls, name_attr)

            if isinstance(attr, Command):
                commands.append(attr)

        return commands


class Commands(ManagerCommand):
    hello = Command("привет", hello_do)
    play_music = Command("включи музыку", play_music_do)
    add_volume = Command("громче", add_volume_do)
    sub_volume = Command("тише", sub_volume_do)
    what_volume = Command("какая громкость", what_volume_do)
    what_time = Command("сколько время", what_time_do)
    stop = Command("стоп", stop_do)
