import matplotlib.pyplot as plt
import numpy as np
import random
import csv

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

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
# output_file = "projekt1/min_data.txt"
# f = open(output_file, 'w')
# f.write("c     min_MSE     min_H       min_var \n")

# Przygotowanie fugur
fig_MSE, (ax_H, ax_var) = plt.subplots(1, 2, figsize=(10, 4))
fig = plt.figure()
ax = fig.add_subplot(111)
# Tworzenie wykresu 3D
fig_3d = plt.figure()
ax0 = fig_3d.add_subplot(111, projection='3d')

c = 2
noise = [ c *(random.random() + random.random() - 1) for _ in range(N)]
triangular_signal_with_noise = [triangular_signal[i] + noise[i]  for i in range(N)]

# minimum value of MSE for H and var
min_MSE_H = c

# plot H - MSE(H)
max = 20

min_var = 0
H = [i for i in range(2,max + 1)]
c = np.linspace(0.2, 5.2, max)
var = np.zeros(len(c))
MSE_H = np.zeros((len(c), len(H)))
MSE_opt = np.zeros(len(c))
H_opt = np.zeros(len(c))
# tswn_optimal = np.zeros(len(c), len(t))
for current_c in range(len(c)):
    noise = [ c[current_c] *(random.random() + random.random() - 1) for _ in range(N)]
    triangular_signal_with_noise = [triangular_signal[i] + noise[i]  for i in range(N)]
    min_MSE = 5
    for current_h in range(len(H)):
        local_Q_sum = np.zeros(N)
        for i in range(N):
            for h in range(H[current_h]):
                if i > H[current_h]:
                    local_Q_sum[i] += triangular_signal_with_noise[i-h] 

        estimated_Q = np.zeros(N)
        estimated_Q =[ local_Q_sum[i]/(H[current_h]) if (i > H[current_h]) else triangular_signal_with_noise[i]  for i in range(N)]

        for i in range(H[current_h], N): # od H do N
            MSE_H[current_c][current_h] += (estimated_Q[i] - triangular_signal[i])**2
        MSE_H[current_c][current_h] = MSE_H[current_c][current_h]/(N - H[current_h])

        if MSE_H[current_c][current_h] < min_MSE:
            MSE_opt[current_c] = MSE_H[current_c][current_h]
            min_MSE = MSE_opt[current_c]
            H_opt[current_c] = H[current_h]
            

    var[current_c] = 2*(c[current_c]**2)/3 
    
    if current_c == max / 10:
        tswn_optimal = triangular_signal_with_noise
        # Wykres MSE od H
        ax_H.scatter(H, MSE_H[current_c], color='b', marker='o')
        ax_H.set_title('Zależność MSE od H')
        ax_H.set_xlabel('H')
        ax_H.set_ylabel('MSE')
    
    
    
# f.write(f"{c}      {min_MSE}       {min_H}     {min_var} \n")
# f.close()
# print(f"Saved min_MSE, min_H, and min_var to {output_file}")   


# Wykres dla szumu
ax.plot(t, triangular_signal, c='r') 
ax.scatter(t, tswn_optimal, c='b', marker='o')
ax.set_title('Triangular Signal')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
# ax.set_ylim(-amplitude - 0.5, amplitude + 0.5) 

# Wykres MSE od wariancji
ax_var.scatter(var, MSE_opt, color='r', marker='o')
ax_var.set_title('Zależność MSE od wariancji dla optymalnego H')
ax_var.set_xlabel('Var')
ax_var.set_ylabel('MSE')

# WYKRES 3D
# Tworzenie współrzędnych X, Y, Z z odpowiednich zmiennych
X, Y = np.meshgrid(H, var)
Z = MSE_H

# Tworzenie wykresu powierzchniowego
ax0.scatter(H_opt, var, MSE_opt, c='red', marker='o', s=30)

norm = plt.Normalize(Z.min(), Z.max())
colors = cm.coolwarm(norm(Z))
rcount, ccount, _ = colors.shape
surf = ax0.plot_surface(X, Y, Z, rcount=rcount, ccount=ccount,
                       facecolors=colors, shade=False)
surf.set_facecolor((0,0,0,0))

# Dodawanie etykiet osi
ax0.set_xlabel('H')
ax0.set_ylabel('var')
ax0.set_zlabel('MSE_H')

# Dodawanie paska kolorów
# cbar = fig.colorbar(surf, shrink=0.5, aspect=5)

# Tworzenie wykresów zależności MSE od H i var


# # Plot data on the first subplot (ax1)
# ax_H.scatter(MSE_opt, H_opt, color='b', marker='o')
# ax_H.set_title('Zależność MSE od optymalnego H')
# ax_H.set_xlabel('H')
# ax_H.set_ylabel('MSE')

# # Plot data on the second subplot (ax2)
# ax_var.scatter(MSE_opt, var, color='r', marker='o')
# ax_var.set_title('Zależność MSE od wariancji')
# ax_var.set_xlabel('Var')
# ax_var.set_ylabel('MSE')

# Adjust the spacing between the subplots
plt.tight_layout()


# Wyświetlenie wykresu
plt.show()

"""
plt.figure(1)
plt.scatter(H, MSE_H, c='b', marker='o')
plt.scatter(min_H, min_MSE, c='r', marker='o', label=f'Min MSE (H={min_H}, MSE={min_MSE})')
plt.title(f'MSE(H) for c = {c}')
plt.xlabel('H')
plt.ylabel('MSE')
plt.show()

plt.figure()
plt.plot(var, MSE_c,c='b', marker='o')
# plt.scatter(min_var, min_MSE_c, c='r', marker='o', label=f'Min MSE (var={min_var}, MSE={min_MSE_c})')
# plt.title(f'MSE(var) for c = {c}')
plt.xlabel('var')
plt.ylabel('MSE')
plt.show()
"""
# print(f"MSE: {min_MSE_H}  H: {min_H}  var: {min_var}")
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
