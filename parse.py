import json
import wave

import vosk

from config import BOT_KEYWORD


def percent_intersect(real_command: list, target_command: list) -> int:
    count_intersect = 0

    if real_command == target_command:
        return 100

    if len(real_command) != len(target_command):
        return 0

    for r_cmd, t_cmd in zip(real_command, target_command):
        if r_cmd == t_cmd:
            count_intersect += len(r_cmd)
            continue

        for r_symbol, t_symbol in zip(r_cmd, t_cmd):
            if r_symbol == t_symbol:
                count_intersect += 1

    one_percent = len(''.join(real_command)) / 100
    percent = int(count_intersect / one_percent)

    return percent


def parse_command(speach: str) -> list:
    res = []

    for word in speach.split(" "):
        res.append(word)

    if BOT_KEYWORD not in res:
        return []

    slice_index = res.index(BOT_KEYWORD)

    res = res[slice_index+1:]

    return res


def recognize_phrase(model: vosk.Model, phrase_wav_path: str) -> str:
    """
    Recognize Russian voice in wav
    """
    wave_audio_file = wave.open(phrase_wav_path, "rb")

    # Проверка, соответствует ли частота дискретизации требованиям
    if wave_audio_file.getframerate() != 24000:
        raise ValueError("Частота дискретизации должна быть 24000 Гц.")

    offline_recognizer = vosk.KaldiRecognizer(model, wave_audio_file.getframerate())

    data = wave_audio_file.readframes(wave_audio_file.getnframes())

    if offline_recognizer.AcceptWaveform(data):
        recognized_data = json.loads(offline_recognizer.Result())["text"]
    else:
        recognized_data = json.loads(offline_recognizer.FinalResult())["text"]

    return recognized_data
