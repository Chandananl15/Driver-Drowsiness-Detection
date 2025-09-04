import numpy as np
from scipy.io.wavfile import write

# Generate a 2-second 440 Hz beep
sample_rate = 44100
duration = 2.0  # seconds
frequency = 440.0  # Hz

t = np.linspace(0, duration, int(sample_rate * duration), False)
tone = np.sin(2 * np.pi * frequency * t) * 0.5

# Convert to 16-bit PCM and save
audio = (tone * 32767).astype(np.int16)
write("alarm.wav", sample_rate, audio)

print("✅ alarm.wav created successfully!")
