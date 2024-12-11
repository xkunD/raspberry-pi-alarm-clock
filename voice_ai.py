import speech_recognition as sr
from filelock import FileLock
import time

# Initialize recognizer
r = sr.Recognizer()
mic = sr.Microphone()

# Files for communication
output_file = "output_file_ai.txt"
trigger_file = "trigger.txt"
lock_output = FileLock(f"{output_file}.lock")
lock_trigger = FileLock(f"{trigger_file}.lock")

print("Voice recognition ready.")


while True:
    try:
        # Check trigger file
        with lock_trigger:
            with open(trigger_file, "r") as f:
                trigger = f.read().strip()

        if trigger == "START":
            print("Listening for voice input...")
            with mic as source:
                r.adjust_for_ambient_noise(source)
                print("Say something...")
                audio = r.listen(source)

            # Recognize speech
            try:
                words = r.recognize_google(audio, language="en-US")
                print("Recognized:", words)

                # Write recognized speech to output file
                with open(output_file, "w") as f:
                    f.write(words)
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError as e:
                print(f"Request error: {e}")
        else:
            # Wait briefly before rechecking the trigger
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nExiting voice recognition.")
        break


