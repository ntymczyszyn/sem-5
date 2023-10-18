import numpy as np
import matplotlib.pyplot as plt

# Parameters of the triangular signal
frequency = 0.005  # Frequency of the signal (cycles per second)
amplitude = 0.5  # Amplitude of the signal
duration = 1000.0  # Duration of the signal (seconds)
sampling_frequency = 1000  # Sampling frequency (samples per second)

# Generate a time vector
t = np.linspace(0, duration, int(sampling_frequency * duration), endpoint=False)

# Generate the triangular signal
triangular_signal = amplitude * (2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1)

# Plot 
plt.figure()
plt.plot(t, triangular_signal)
plt.title('Triangular Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()
