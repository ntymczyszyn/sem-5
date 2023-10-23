import matplotlib.pyplot as plt
import numpy as np
import random

# parameters 
frequency = 0.005  # Frequency of the signal (cycles per second)
amplitude = 1.0  # Amplitude of the signal
duration = 1000.0  # Duration of the signal (seconds)
sampling_frequency = 0.15  # Sampling frequency (samples per second)

# time vector
t = np.linspace(0, duration, int(sampling_frequency * duration), endpoint=False) # <class 'numpy.ndarray'>

# triangular signal - is it corect computation? 
triangular_signal = amplitude * (2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1)
# test = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1

c = 0.3
H = 2
noise = [ c *(random.random() + random.random() - 1) for _ in range(len(t))]
triangular_signal_with_noise = [triangular_signal[i] + noise[i]  for i in range(len(t))]

# the estimated value of the unknow Q variable
# adds H elements to get sum
sum_Q = np.zeros(len(t))
for i in range(len(t)):
    for j in range(H):
        if i > H:
            sum_Q[i] += triangular_signal_with_noise[i-j] 
estimated_Q = np.zeros(len(t))
# the average sum to get the estimated value of Q
estimated_Q =[ sum_Q[i]/(H) if (i > H) else 0.5 for i in range(len(t))]

# the difference between Estimated Q and given value
MSE = 0
for i in range(len(t)):
    MSE += (triangular_signal_with_noise[i] - estimated_Q[i])*(triangular_signal_with_noise[i] - estimated_Q[i]) 
MSE = MSE/len(t)
print(MSE)
"""
plt.figure()
plt.plot(t, triangular_signal, c='r') 
plt.scatter(t, triangular_signal_with_noise, c='b', marker='o')
plt.title('Triangular Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.ylim(-amplitude - 0.5, amplitude + 0.5) 
plt.show()
"""
plt.figure()
plt.plot(t, triangular_signal, c='r')
plt.plot(t, estimated_Q, c='b', marker='o')
plt.show()
