import matplotlib.pyplot as plt
import numpy as np
import random
import csv

# parameters 
frequency = 0.005  # Frequency of the signal (cycles per second)
amplitude = 1.0  # Amplitude of the signal
duration = 1000.0  # Duration of the signal (seconds)
sampling_frequency = 0.8  # Sampling frequency (samples per second)

# time vector
t = np.linspace(0, duration, int(sampling_frequency * duration), endpoint=False) # <class 'numpy.ndarray'>
N = len(t)
# triangular signal - is it corect computation? 
triangular_signal = amplitude * (2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1)
# test = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1


# write data to CSV
output_file = "min_data.txt"
f = open(output_file, 'w')
f.write("c     min_MSE     min_H       min_var \n")

# c = 4
for c in range(1, 10):
    noise = [ c *(random.random() + random.random() - 1) for _ in range(N)]
    triangular_signal_with_noise = [triangular_signal[i] + noise[i]  for i in range(N)]

    # minimum value of MSE for H and var
    min_MSE = c

    # plot H - MSE(H)
    max = 100
    H = [i for i in range(2,max + 1)]
    MSE = np.zeros(len(H))
    var = np.zeros(len(H))
    for m in range(len(H)):
        local_Q_sum = np.zeros(N)
        for i in range(N):
            for h in range(H[m]):
                if i > H[m]:
                    local_Q_sum[i] += triangular_signal_with_noise[i-h] 

        estimated_Q = np.zeros(N)
        estimated_Q =[ local_Q_sum[i]/(H[m]) if (i > H[m]) else triangular_signal_with_noise[i]  for i in range(N)]

        for i in range(H[m],N):
            var[m] += (estimated_Q[i] -triangular_signal[i]**2)**2
        var[m] = var[m]/(N - H[m])
        for i in range(H[m], N): # od H do N
            MSE[m] += (estimated_Q[i] - triangular_signal[i])**2
        MSE[m] = MSE[m]/(N - H[m])
        if MSE[m] < min_MSE:
            min_MSE = MSE[m]
            min_H = H[m] # something goes wrong here
            min_var = var[m]

    # Write data to CSV
    f.write(f"{c}      {min_MSE}       {min_H}     {min_var} \n")

f.close()
# print(f"Saved min_MSE, min_H, and min_var to {output_file}")   


plt.figure(1)
plt.scatter(H, MSE, c='b', marker='o')
plt.scatter(min_H, min_MSE, c='r', marker='o', label=f'Min MSE (H={min_H}, MSE={min_MSE})')
plt.title(f'MSE(H) for c = {c}')
plt.xlabel('H')
plt.ylabel('MSE')
plt.show()

plt.figure(2)
plt.scatter(var, MSE,c='b', marker='o')
plt.scatter(min_var, min_MSE, c='r', marker='o', label=f'Min MSE (var={min_var}, MSE={min_MSE})')
plt.title(f'MSE(var) for c = {c}')
plt.xlabel('var')
plt.ylabel('MSE')
plt.show()

print(f"MSE: {min_MSE}  H: {min_H}  var: {min_var}")
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


# plt.figure(figsize=(12, 8))  
# plt.plot(t, triangular_signal, c='r')
# plt.plot(t, estimated_Q, c='b', marker='o')
# plt.scatter(t, triangular_signal_with_noise, c='g')
# plt.show()
# # -------------------------------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(14, 5))
axs[0].plot(t, triangular_signal, c='r')
axs[0].plot(t, estimated_Q, c='b', marker='o')
axs[0].scatter(t, triangular_signal_with_noise, c='g')
axs[0].set_title('Triangular Wave with the estimate')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('Amplitude')

# axs[1].plot(t, estimated_Q, c='b')
# axs[1].plot(t, triangular_signal_with_noise, c='g')
# axs[1].set_title('Noisy Triangular Wave and the estimate')
axs[1].scatter(H, MSE, c='b', marker='o')
axs[1].set_title(f'MSE(H) for c = {c}')
axs[1].set_xlabel('H')
axs[1].set_ylabel('MSE')
# axs[1].set_xlabel('Time')
# axs[1].set_ylabel('Amplitude')
plt.tight_layout()  
plt.show()
#------------------------------------------------------------
# theta_circumflex = "\u0302\u03B8*"  # Kombinacja θ (theta) i daszka
# print(theta_circumflex)
"""