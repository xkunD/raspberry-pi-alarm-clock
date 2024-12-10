import vlc
import time
import os

# File to check for alarm trigger
alarm_trigger_file = "alarm_trigger.txt"

# Initialize VLC MediaPlayer
p = vlc.MediaPlayer("cliped_alarm.mp3")

# Function to clear the alarm trigger
def clear_alarm_trigger():
    with open(alarm_trigger_file, "w") as f:
        f.write("")

print("Alarm is running. Listening for triggers...")

while True:
    if os.path.exists(alarm_trigger_file):
        with open(alarm_trigger_file, "r") as f:
            trigger = f.read().strip()

        if trigger == "RING":
            print("Alarm triggered! Playing alarm...")
            start_time = time.time()
            while time.time() - start_time < 10:  # Loop for 5 seconds
                p.play()  # Start playing the audio
                time.sleep(1)  # Allow the audio to play for its duration
                if p.get_state() == vlc.State.Ended:
                    p.stop()  # Ensure playback is stopped before restarting
            clear_alarm_trigger()  # Reset the trigger
    time.sleep(1)  # Check for the trigger every second
