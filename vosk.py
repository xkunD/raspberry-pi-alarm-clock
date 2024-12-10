import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

# Load the Vosk model
model = Model("path/to/vosk-model")  # Replace with your model path

# Initialize recognizer
recognizer = KaldiRecognizer(model, 16000)

# Function to capture and process audio
print("Speak now...")
with sd.InputStream(samplerate=16000, channels=1, dtype='int16') as stream:
    while True:
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print(result.get("text"))
