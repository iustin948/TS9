import wave
import numpy as np
import sounddevice as sd
from scipy import signal
from scipy.signal import butter, lfilter
def simulate_overdrive(input_signal, drive=0.1, tone=0.5, level=0.5, sample_rate=44100):
    # Pre-calculate variables
    gain = 1.0 + drive * 4.0
    tone_control = 1.0 + (2.0 * (1.0 - tone))

    # Apply distortion effect with soft clipping
    output_signal = np.clip(input_signal * gain, -1, 1)
    output_signal = np.sign(output_signal) * (1 - np.exp(-np.abs(output_signal)))

    # Apply tone control
    output_signal *= tone_control

    # Apply output level control
    output_signal *= level

    # Normalize the output signal
    output_signal /= np.max(np.abs(output_signal))

    return output_signal

def simulate_guitar_cabinet(input_signal, sample_rate, level=0.8):
    # Apply cabinet simulation EQ
    output_signal = np.copy(input_signal)

    # Apply high-cut filter
    cutoff_freq = 6000.0  # Adjust cutoff frequency as desired
    nyquist_freq = 0.5 * sample_rate
    b, a = butter(2, cutoff_freq / nyquist_freq, btype='high')
    output_signal = lfilter(b, a, output_signal)

    # Apply low-cut filter
    cutoff_freq = 100.0  # Adjust cutoff frequency as desired
    b, a = butter(2, cutoff_freq / nyquist_freq, btype='low')
    output_signal = lfilter(b, a, output_signal)

    # Apply output level control
    output_signal *= level

    # Normalize the output signal
    output_signal /= np.max(np.abs(output_signal))

    return output_signal
# Open the WAV file
from scipy.io.wavfile import read, write
a = read("input.wav")

# Convert the raw audio data to a NumPy array
audio_array = np.array(a[1])
print(audio_array)

output_signal = simulate_overdrive(audio_array,0,0,0.5)
last = simulate_guitar_cabinet(output_signal,44100)
# Play the audio
write("output.wav", 44100, last)
sd.play(last, 44100)
sd.wait()
