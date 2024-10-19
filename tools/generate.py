import threading
import wave

import pyaudio
import pyttsx3
import numpy as np

from state.context import Context
from state.manager import StateManager
from state.states import State


def say(text: str):
    with threading.Lock():
        volume = Context.volume

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    try:
        engine.endLoop()
    except RuntimeError:
        pass

    # Set the speed and volume of the voice
    engine.setProperty('rate', 150)  # 150 words per minute
    engine.setProperty('volume', volume)  # 70% volume

    # Convert the text to speech
    engine.say(text)
    engine.runAndWait()


def play_file(sound: str):
    CHUNK = 1024

    with wave.open(sound, 'rb') as wf:
        # Instantiate PyAudio and initialize PortAudio system resources
        p = pyaudio.PyAudio()

        # Open stream
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Read and play samples from the wave file
        while True:
            with threading.Lock():
                if StateManager.actual_state is State.music_off:
                    StateManager.actual_state = None
                    break

            data = wf.readframes(CHUNK)
            if not data:
                break

            # Convert data to numpy array for volume adjustment
            samples = np.frombuffer(data, dtype=np.int16)

            with threading.Lock():
                volume = Context.volume

            # Adjust volume
            samples = (samples * volume).astype(np.int16)  # Scale the samples

            # Write adjusted samples to the stream
            stream.write(samples.tobytes())

        with threading.Lock():
            if StateManager.actual_state is State.music_is_run:
                StateManager.actual_state = None

        # Close stream
        stream.close()

        # Release PortAudio system resources
        p.terminate()
