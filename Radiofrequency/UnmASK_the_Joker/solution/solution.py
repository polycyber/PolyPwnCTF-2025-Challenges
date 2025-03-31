from scipy.io.wavfile import read
import numpy as np

sample_rate, signal = read("output_signal.wav")
symbole_rate = 50e3

signal = 255 * signal.astype(np.float64) / np.iinfo(signal.dtype).max

binary_data = b''
n_symbol = int(sample_rate/symbole_rate)
for i in range(0, len(signal), n_symbol):
    binary_data += bytes([int(np.ceil(np.max(signal[i:i+n_symbol])))])

with open('decoded.png', 'wb') as file:
    file.write(binary_data)