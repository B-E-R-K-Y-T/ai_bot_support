from commands import Commands
from parse import percent_intersect


def run_command(real_command: list):
    for command in Commands.get_commands():
        percent = percent_intersect(real_command, command.command)

        if percent >= 70:
            command.execute()
            break
    else:
        Commands.DEFAULT_DO.execute()
