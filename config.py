import pyaudio
import vosk

BOT_KEYWORD = "добряк"
MODEL = vosk.Model("data/vosk-model-small-ru-0.22")

CHUNK = 12000
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 24000
WAVE_OUTPUT_FILENAME = "output.wav"

