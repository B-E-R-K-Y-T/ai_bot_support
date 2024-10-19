import wave
import pyaudio

from config import FORMAT, CHANNELS, RATE, CHUNK, WAVE_OUTPUT_FILENAME


def get_listener():
    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=2,
        frames_per_buffer=CHUNK
    )

    def listen(record_seconds: int = 4):
        write_audio(record_seconds, p, stream)

    return listen


def write_audio(record_seconds: int, p: pyaudio.PyAudio, stream: pyaudio.PyAudio.Stream):
    print("* recording")
    frames = []

    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")
    # stream.stop_stream()
    # stream.close()
    # p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
