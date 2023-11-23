import matplotlib.pyplot as plt
import numpy as np
import random
import os
from matplotlib import cm

def preparing_data(signal_IN, t, b_true):
    N = len(t)
    V_true = np.zeros(N)
    signal_OUT = np.zeros(N)
    for k in range(2, N):
        # True variables, that we get
        # triangular noise
        noise = [ 8 *(random.random() + random.random() - 1) for _ in range(N)]
        # Signal without noise
        V_true[k] =  (b_true[0]*signal_IN[k] + b_true[1]*signal_IN[k-1] + b_true[2]*signal_IN[k-2])
        # Output signal
        signal_OUT[k] = V_true[k] + noise[k]
    return signal_OUT, V_true

def simulation(signal_IN, t,  b_true, Lambda):
    N = len(t)
    signal_OUT, V_true = preparing_data(signal_IN, t, b_true)
    
    P_k = np.array([[1000, 0, 0],
                    [0, 1000, 0],
                    [0, 0, 1000]])

    b_estimated = np.array([[0],
                            [0],
                            [0]])
    
    V_k = np.zeros(N)
    estimated_with_noise = np.zeros(N)
    MSE_sum = 0
    MSE_sum2 = 0
    for k in range(2, N):
        # triangular noise - to get different one than original
        noise = [ 8*(random.random() + random.random() - 1) for _ in range(N)]

        # Calculate b_estimated based on Input and Output
        # Wejscia - regresor ??
        Q = np.array([[signal_IN[k]],
                      [signal_IN[k-1]],
                      [signal_IN[k-2]]])
        
        # Wyjścia (czemu 3?)
        y_3 = np.array([[signal_OUT[k]],
                        [signal_OUT[k-1]],
                        [signal_OUT[k-2]]])

        # Calculate P_k - macierz kowariancji
        new_P_k = 1/Lambda * (P_k - (P_k @ Q @ Q.T @ P_k) / (Lambda + Q.T @ P_k @ Q))
        P_k = new_P_k

        # Calculate b_estimated  -- tutaj dla y_3 działa słabo, dla y_3[0] działa perfekcyjnie XDD
        new_b_estimated = b_estimated + P_k @ Q * (y_3[0] - Q.T @ b_estimated)
        b_estimated = new_b_estimated
     
        V_k[k] =  (b_estimated[0][0]*signal_IN[k] + b_estimated[1][0]*signal_IN[k-1] + b_estimated[2][0]*signal_IN[k-2])
        estimated_with_noise[k] = V_k[k] + noise[k]

        MSE_sum += (np.abs(V_k[k] - signal_OUT[k]))**2
        MSE_sum2 += (np.abs(estimated_with_noise[k] - signal_OUT[k]))**2


    MSE = MSE_sum/(N-2)
    MSE2 = MSE_sum2/(N-2)
    print(b_estimated)
    print(f"MSE dla Lambdy = {Lambda} : {MSE}")
    print(f"MSE2 dla Lambdy = {Lambda} : {MSE2}")
    return V_k, V_true, estimated_with_noise, signal_OUT, MSE, MSE2
    

def image(t, signal_IN, b_true, Lambda):
    V_k, V_true, estimated_with_noise, signal_OUT, MSE, MSE2 = simulation(signal_IN, t,  b_true, Lambda)
    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(111)
    ax.plot(t, V_k, c='b', label="Estymowana fala") 
    # ax.plot(t, V_true, c='r', label="Fala trójkątna bez szumu")
    ax.scatter(t, V_k, c='b', marker="o", s=10, label="Estymowana fala") 
    # ax.scatter(t, V_true, c='r', marker="o", s=10, label="Fala trójkątna bez szumu")
    # ax.scatter(t, estimated_with_noise, c='r', marker="o", label="Estymowana fala + szum")  
    # ax.scatter(t, signal_OUT, c='g', marker="o", label="Zaszumiona fala trójkątna")
    # ax.plot(t, estimated_with_noise, c='r', label="Estymowana fala + szum")  
    ax.plot(t, signal_OUT, c='g', label="Zaszumiona fala trójkątna")
    ax.set_title(f'Estymowana i zaszumiona fala dla Lamby = {Lambda}')
    ax.legend(loc='upper right')
    ax.set_xlabel('Czas (s)')
    ax.set_ylabel('Amplituda')
    fig.savefig(os.path.join(os.path.dirname(__file__), "images_test", f"Estymowana_Lambda={Lambda}.png"))


def image_MSE(t, signal_IN, b_true, Lambda):
    MSE = np.zeros(len(Lambda))
    MSE2 = np.zeros(len(Lambda))
    for i in range(len(Lambda)):
        V_k, V_true, estimated_with_noise, signal_OUT, mse, mse2 = simulation(signal_IN, t,  b_true, Lambda[i])
        MSE[i] = mse
        MSE2[i] = mse2
    
    fig_MSE = plt.figure(figsize=(14,6))
    ax_MSE = fig_MSE.add_subplot(121)
    ax_MSE.plot(Lambda, MSE)
    ax_MSE.set_title(f'MSE  od Lambdy')
    ax_MSE.legend(loc='upper right')
    ax_MSE.set_xlabel('Czas (s)')
    ax_MSE.set_ylabel('Amplituda')

    ax_MSE2 = fig_MSE.add_subplot(122)
    ax_MSE2.plot(Lambda, MSE)
    ax_MSE2.set_title(f'MSE  od Lambdy')
    ax_MSE2.legend(loc='upper right')
    ax_MSE2.set_xlabel('Czas (s)')
    ax_MSE2.set_ylabel('Amplituda')
    fig_MSE.savefig(os.path.join(os.path.dirname(__file__), "images_test", f"MSE.png"))


# ZNANE
# signal_IN
# -> u_k -- wartość na wejściu 
# signal_OUT -> y_3 -- wartość na wyjściu
# SZUKANE
# b_true -> poprzez b_estimated
# INNE
# V_k -> sygnał po wyjściu z obiektu, którym mamy "sterować" 
def main():
    # triangular function parameters 
    frequency = 0.01  # Frequency of the signal_IN(cycles per second)
    period = 1 / frequency
    amplitude = 1.0  # Amplitude of the signal_IN

    duration = 500.0  # Duration of the signal_IN(seconds)
    sampling_frequency = 0.25 # Sampling frequency (samples per second)
    
    # time vector
    t = np.linspace(0, duration, int(sampling_frequency * duration), endpoint=False) # <class 'numpy.ndarray'>
    signal_IN = ((4 * amplitude) / period) * np.abs(((t - (period * 0.25))%period) - (period * 0.5)) - amplitude
    # signal_IN = amplitude * np.sin(2 * np.pi * random.random() * t)
    # signal_IN = [ random.random()-0.5 for _ in range(len(t))]

    Lambda = [1, 0.8]
    b_0, b_1, b_2 = 12, 2, 0.5
    b_true = [b_0, b_1, b_2] # powinna być macierz pionowa, ale nie chce mi sie tego komplikować po adekwatność do zadania, jak kod działa tak samo
    
    for i in range(len(Lambda)):
        image(t, signal_IN, b_true, Lambda[i])

    # image_MSE(t, signal_IN, b_true, Lambda)
    
if __name__ == "__main__":
    main()

