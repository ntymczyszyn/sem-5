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

def preparing_data(signal, t):
    N = len(t)
    b_0, b_1, b_2 = 1, 1, 1
    b_true = [b_0, b_1, b_2] # powinna być macierz pionowa, ale nie chce mi sie tego komplikować po adekwatność do zadania, jak kod działa tak samo
 
    V_k = np.zeros(N)
    signal_with_noise = np.zeros(N)
    for k in range(N):
        if( k >= 2):
            noise = [ 0.5 *(random.random() + random.random() - 1) for _ in range(N)]
            V_k[k] = 1/3 * (b_true[0]*signal[k] + b_true[1]*signal[k-1] + b_true[2]*signal[k-2])
            signal_with_noise[k] = V_k[k] + noise[k]

    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(111)
    ax.plot(t, V_k, c='r', label="Prawdziwa fala bez szumu")  
    ax.scatter(t, signal_with_noise, c='g', marker='o', label="Zaszumiona fala trójkątna")
    ax.set_title(f'Prawdziwa i zaszumiona fala')
    ax.legend(loc='upper right')
    ax.set_xlabel('Czas (s)')
    ax.set_ylabel('Amplituda')
    fig.savefig(os.path.join(os.path.dirname(__file__), "images_test", "Prawdziwa.png"))
    return signal_with_noise, noise

def simulation(N, signal, signal_with_noise, t, noise, Lambda):
    P_k = np.array([[100, 0, 0],
                    [0, 100, 0],
                    [0, 0, 100]])

    b_estimated = np.array([[0],
                            [0],
                            [0]])
    V_k = np.zeros(N)
    for k in range(2, N):
        Q = np.array([[signal[k]],
                      [signal[k-1]],
                      [signal[k-2]]])

        y_k = np.array([[signal_with_noise[k]],
                        [signal_with_noise[k-1]],
                        [signal_with_noise[k-2]]])

        # Obliczenia P_k
        new_P_k = 1/Lambda * (P_k - (P_k @ Q @ Q.T @ P_k) / (Lambda + Q.T @ P_k @ Q))
        P_k = new_P_k

        # Obliczenia b_estimated
        new_b_estimated = b_estimated + P_k @ Q * (y_k - Q.T @ b_estimated)
        b_estimated = new_b_estimated

    # Tworzenie nowego sygnału
    estimated_output = np.zeros(N)
    V_true = np.zeros(N)
    b_0, b_1, b_2 = 1, 1, 1
    b_true = [b_0, b_1, b_2]
    for k in range(2,N): 
        V_k[k] = 1/3 * (b_estimated[0][0]*signal[k] + b_estimated[1][0]*signal[k-1] + b_estimated[2][0]*signal[k-2])
        V_true[k] = 1/3 * (b_true[0]*signal[k] + b_true[1]*signal[k-1] + b_true[2]*signal[k-2])
        # estimated_output[k] = V_k[k] + noise[k]
    print(b_estimated)

    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(111)
    ax.plot(t, V_k, c='b', label="Estymowana fala") 
    ax.plot(t, V_true, c='orange', label="Fala trójkątna bez szumu")
    # ax.plot(t, estimated_output, c='r', label="Estymowana fala + szum")  
    # ax.plot(t, signal_with_noise, c='g', label="Zaszumiona fala trójkątna")
    ax.set_title(f'Estymowana i zaszumiona fala')
    ax.legend(loc='upper right')
    ax.set_xlabel('Czas (s)')
    ax.set_ylabel('Amplituda')
    fig.savefig(os.path.join(os.path.dirname(__file__), "images_test", "Estymowana.png"))


# ZNANE
# signal -> u_k -- wartość na wejściu 
# signal_with_noise -> y_k -- wartość na wyjściu
# SZUKANE
# b_true -> poprzez b_estimated
# INNE
# V_k -> sygnał po wyjściu z obiektu, którym mamy "sterować" 
def main():
    # triangular function parameters 
    frequency = 0.01  # Frequency of the signal (cycles per second)
    period = 1 / frequency
    amplitude = 1.0  # Amplitude of the signal
    duration = 500.0  # Duration of the signal (seconds)
    sampling_frequency = 0.5 # Sampling frequency (samples per second)
    
    # time vector
    t = np.linspace(0, duration, int(sampling_frequency * duration), endpoint=False) # <class 'numpy.ndarray'>
    N = len(t)
    signal = ((4 * amplitude) / period) * np.abs(((t - (period * 0.25))%period) - (period * 0.5)) - amplitude

    signal_with_noise, noise = preparing_data(signal, t)

    simulation(N, signal, signal_with_noise, t, noise, Lambda = 1)

    
if __name__ == "__main__":
    main()

