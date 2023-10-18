import matplotlib.pyplot as plt
import numpy as np
import random

# parameters 
frequency = 0.005  # Frequency of the signal (cycles per second)
amplitude = 0.5  # Amplitude of the signal
duration = 1000.0  # Duration of the signal (seconds)
sampling_frequency = 1000  # Sampling frequency (samples per second)

# time vector
#t = np.linspace(0, duration, int(sampling_frequency * duration), endpoint=False)
t = np.linspace(0, duration, 100, endpoint=False)

# triangular signal
triangular_signal = amplitude * (2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1)
test = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
c = 1
noise = c *(random.random() + random.random() - 1)

plt.figure()
plt.plot(t, triangular_signal, 'r')
plt.scatter(t, triangular_signal, c='b', marker='o')
plt.title('Triangular Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.ylim(-amplitude - 0.5, amplitude + 0.5) 
plt.show()
