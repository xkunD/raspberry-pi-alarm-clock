import speech_recognition as sr
from datetime import date
from gpiozero import LED
from time import sleep

# Uncomment if you have the hardware setup
# red = LED(17)
# relay1 = LED(14)
# relay2 = LED(15)

# Initialize recognizer
r = sr.Recognizer()

# List available microphones and set the device index
print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")
mic = sr.Microphone(device_index=1)  # Replace with the correct index

print("Hello, ready to listen!")

# Main loop
while True:
    try:
        with mic as source:
            print("Adjusting for ambient noise, please wait...")
            r.adjust_for_ambient_noise(source)
            print("Say something...")
            audio = r.listen(source)  # Listen for the user's speech

        # Recognize speech
        try:
            words = r.recognize_google(audio, language="en-US")  # Change language if needed
            print("You said:", words)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            continue  # Skip to the next iteration
        except sr.RequestError as e:
            print(f"Request error from Google Speech Recognition service: {e}")
            break  # Exit on API failure

        # Perform actions based on recognized words
        if words.lower() == "today":
            print(f"Today's date is: {date.today()}")
        elif words.lower() == "exit":
            print("Exiting...")
            sleep(1)
            print("Goodbye!")
            break

        # Uncomment these lines to control hardware
        # elif words.lower() == "led on":
        #     red.on()
        # elif words.lower() == "led off":
        #     red.off()
        # elif words.lower() == "relay one on":
        #     relay1.on()
        # elif words.lower() == "relay one off":
        #     relay1.off()
        # elif words.lower() == "relay two on":
        #     relay2.on()
        # elif words.lower() == "relay two off":
        #     relay2.off()

    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        break
