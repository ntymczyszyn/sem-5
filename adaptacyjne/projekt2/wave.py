import matplotlib.pyplot as plt
import numpy as np
import random
import os
from matplotlib import cm

# number of samples, max h, expected signal 
def calculate_all(N, max, triangular_signal):
    H = [i for i in range(2,max + 2)]
    c = np.linspace(0.05, 1.05, max) 
    var = np.zeros(len(c))
    MSE = np.zeros((len(c), len(H)))
    MSE_opt = np.zeros(len(c))
    H_opt = np.zeros(len(c))
    for current_c in range(len(c)):
        # max value that MSE can be - for finding H opt
        min_MSE = 5    
        var[current_c] = 2*(c[current_c]**2)/3 
        for current_h in range(len(H)):
            noise = [ c[current_c] *(random.random() + random.random() - 1) for _ in range(N)]
            triangular_signal_with_noise = [triangular_signal[i] + noise[i]  for i in range(N)]
            local_sum = np.zeros(N)
            for i in range(N):
                for h in range(H[current_h]):
                    if i > H[current_h]:
                        local_sum[i] += triangular_signal_with_noise[i-h] 
            estimated = np.zeros(N)
            estimated =[ local_sum[i]/(H[current_h]) if (i > H[current_h]) else triangular_signal_with_noise[i]  for i in range(N)]
           
            for i in range(H[current_h], N): # from H till N
                MSE[current_c][current_h] += (estimated[i] - triangular_signal[i])**2
            MSE[current_c][current_h] = MSE[current_c][current_h]/(N - H[current_h])
            # serching for min MSE for each var
            if MSE[current_c][current_h] < min_MSE:
                MSE_opt[current_c] = MSE[current_c][current_h]
                min_MSE = MSE_opt[current_c]
                H_opt[current_c] = H[current_h]      
        
    return H, MSE, var, H_opt, MSE_opt
   
    
def estimate(triangular_signal, N, c, H):
    noise = [ c *(random.random() + random.random() - 1) for _ in range(N)]
    triangular_signal_with_noise = [triangular_signal[i] + noise[i]  for i in range(N)]
    MSE = 0
    local_sum = np.zeros(N)
    for i in range(N):
        for h in range(H):
            if i > H:
                local_sum[i] += triangular_signal_with_noise[i-h] 
    estimated = np.zeros(N)
    estimated =[ local_sum[i]/(H) if (i > H) else triangular_signal_with_noise[i]  for i in range(N)]

    for i in range(H, N): # od H do N
        MSE += (estimated[i] - triangular_signal[i])**2
    MSE = MSE/(N - H)
    return triangular_signal_with_noise, estimated, MSE


def main():
    # triangular function parameters 
    frequency = 0.01  # Frequency of the signal (cycles per second)
    period = 1 / frequency
    amplitude = 1.0  # Amplitude of the signal
    duration = 1000.0  # Duration of the signal (seconds)
    sampling_frequency = 0.5 # Sampling frequency (samples per second)
    
    # time vector
    t = np.linspace(0, duration, int(sampling_frequency * duration), endpoint=False) # <class 'numpy.ndarray'>
    N = len(t)

    triangular_signal = ((4 * amplitude) / period) * np.abs(((t - (period * 0.25))%period) - (period * 0.5)) - amplitude

    H, MSE, var, H_opt, MSE_opt = calculate_all(N, max, triangular_signal)
    t_w_n, est, MSE = estimate(triangular_signal, N, c=0.4, H=5)

    # u_true = [u_0, u_1, u_3]
    # b_true = [b_0, b_1, b_2]
    # V_k = b_true[0]*u_true[0] + b_true[1]*u_true[1] + b_true[2]*u_true[2]
    # y_k = v_k + z_k
    
    
if __name__ == "__main__":
    main()

