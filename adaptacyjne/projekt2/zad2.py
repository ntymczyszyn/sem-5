import matplotlib.pyplot as plt
import numpy as np
import random
import os
from matplotlib import cm

C = 0.5 
images_folder = "images_test2"


def simulation(N, b_true, Lambda):    
    P_k = np.array([[100, 0, 0],
                    [0, 100, 0],
                    [0, 0, 100]])
    print(f"lambda = {Lambda}")
    b_estimated = np.zeros((3,N))
    V_estimated = np.zeros(N)
    y_estimated = np.zeros(N)
    V_true = np.zeros(N) # prawdziwe wyjście z obiektu bez zakłócenia
    y_true = np.zeros(N) # prawdziwe wyjście z zakłóceniem
    u_k = np.random.uniform(0, 3, N)
    Phi = np.array([[u_k[0]],
                    [0],
                    [0]])
    # Tworzenie zakłócenia
    noise = [C *(random.random() + random.random() - 1) for _ in range(N)]

    previous_b_est = [ [0],
                    [0],
                    [0]]

    for k in range(N):
        # Wyliczamy nowe wyjście na podstawie oczekiwanego wejścia?? z b_true
        # V_true[k] = (b_true[0]*u_calculated[k] + b_true[1]*u_calculated[k-1] + b_true[2]*u_calculated[k-2])
        V_true[k] = np.dot(Phi.T, b_true[:,k])
        y_true[k] = V_true[k] + noise[k]

        # Calculate P_k - macierz kowariancji P_k to P(k-1) a new_P_k to P(k)
        P_k = 1/Lambda * (P_k - (np.dot(np.dot(np.dot(P_k,Phi),Phi.T),P_k))/ (Lambda + np.dot(np.dot(Phi.T, P_k),Phi)))

        # Calculate b_estimated 
        if k > 0:
            previous_b_est = [[b_estimated[0, k-1]],
                        [b_estimated[1, k-1]],
                        [b_estimated[2, k-1]]]
            b_estimated[:,k] = (previous_b_est + (y_true[k] - np.dot(Phi.T, previous_b_est)) * np.dot(P_k,Phi)).reshape((3,)) 
            
        #V_estimated[k] =  (b_estimated[0, k]*u_calculated[k] + b_estimated[1, k]*u_calculated[k-1] + b_estimated[2, k]*u_calculated[k-2])
        V_estimated[k] = np.dot(Phi.T, b_estimated[:,k])
        y_estimated[k] = V_estimated[k] + noise[k]
        if k < N - 1:
                Phi[2,0] = Phi[1,0]
                Phi[1,0] = Phi[0,0]
                Phi[0,0] = u_k[k+1]
                    

    print(f"B = {b_estimated[:,N-1]}")    
    return V_true, V_estimated, y_true, y_estimated, b_estimated
    

def zad2(t, b_true, Lambda):
    V_true, V_estimated, y_true, y_estimated, b_estimated = simulation(len(t), b_true, Lambda)
    
    fig_est = plt.figure(figsize=(14, 6))
    ax_est = fig_est.add_subplot(111)
    ax_est.plot(t, b_estimated[0], c='r', label="Estymowane b0 od Lambdy")  #marker="o", s=10,
    ax_est.plot(t, b_true[0], c='black') 
    ax_est.plot(t, b_estimated[1], c='b', label="Estymowane b1 od Lambdy")
    ax_est.plot(t, b_true[1], c='black') 
    ax_est.plot(t, b_estimated[2], c='g', label="Estymowane b2 od Lambdy") 
    ax_est.plot(t, b_true[2], c='black') 
    ax_est.set_title(f'Estymator b^ dla Lambdy = {Lambda}')
    # ax_est.legend(loc='')
    ax_est.set_xlabel('Czas (s)')
    ax_est.set_ylabel('Amplituda')
    ax_est.grid(True)
    # ax_est.set_ylim(0, 5)
    fig_est.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"B_estymowane_lambda={Lambda}.png"))


def main():
    # triangular function parameters 
    frequency = 0.01  # Frequency of the signal (cycles per second)
    period = 1 / frequency
    amplitude = 1.0  # Amplitude of the signal

    duration = 1000.0  # Duration of the u_k(seconds)
    N = 1000 # Amount of samples
    t = np.linspace(0, duration, N, endpoint=False) # <class 'numpy.ndarray'>
    # u_k = np.random.uniform(0, 3,  N)
    Lambda = [1, 0.98, 0.95, 0.9, 0.8]
    param0 = [1.0 for _ in range(len(t))]
    param1 = [2.0 for _ in range(len(t))]
    param2 = [3.0 for _ in range(len(t))]
    b_true =  np.array([param0, param1, param2])
# =================================================================================
    amplituda_min = 1
    amplituda_max = 1.2
    czestotliwosc = 0.005  # Dla przykładu, możesz dostosować według potrzeb
    czas_trwania = duration
    ilosc_probek = N
    # Generowanie czasu i wartości funkcji prostokątnej
    czas = np.linspace(0, czas_trwania, ilosc_probek)
    funkcja_prostokatna = (amplituda_min + (amplituda_max - amplituda_min) / 2 * np.sign(np.sin(2 * np.pi * czestotliwosc * czas)))
    # print(funkcja_prostokatna)
# ================================================================================
    # b_true[0] = [float(funkcja_prostokatna[i]) for i in range(len(t))]
    b_true[0] = funkcja_prostokatna
    # print(b_true[0])
    zad2(t, b_true,  0.95)

    
if __name__ == "__main__":
    main()