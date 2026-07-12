import sounddevice as sd
import numpy as np
import webbrowser
import time

# --- CONFIGURATION ---
THRESHOLD = 20.0       # Volume level to register as a clap (Tweak this!)
CLAP_MAX_DELAY = 0.8   # Maximum seconds allowed between two claps
CLAP_MIN_DELAY = 0.1   # Minimum seconds to avoid one long sound counting twice
COOLDOWN = 3.0         # Cooldown after opening YouTube (so it doesn't open 5 tabs)

# --- STATE VARIABLES ---
clap_count = 0
last_clap_time = 0

def audio_callback(indata, frames, time_info, status):
    global clap_count, last_clap_time
    
    if status:
        print(status)
        
    # Calculate the volume (Root Mean Square) of the current audio chunk
    volume_norm = np.linalg.norm(indata) * 10
    
    current_time = time.time()
    
    # If the sound is louder than our threshold
    if volume_norm > THRESHOLD:
        # Check if enough time passed since the last loud noise
        if (current_time - last_clap_time) > CLAP_MIN_DELAY:
            
            # If it's been too long since the first clap, reset the count
            if (current_time - last_clap_time) > CLAP_MAX_DELAY:
                clap_count = 1
                print("First clap detected! Listening for second...")
            else:
                clap_count += 1
                print("Second clap detected!")
                
            last_clap_time = current_time
            
            # If we hit 2 claps, trigger the action
            if clap_count == 2:
                print("Opening YouTube!")
                webbrowser.open("https://www.youtube.com")
                clap_count = 0 # Reset
                time.sleep(COOLDOWN) # Pause listening briefly

print("Listening for claps... Press Ctrl+C to stop.")

# Open the microphone stream and keep it running
with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100):
    while True:
        time.sleep(0.1) # Keep the main thread alive