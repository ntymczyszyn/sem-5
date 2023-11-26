import matplotlib.pyplot as plt
import numpy as np
import random
import os
from matplotlib import cm

C = 0.5 # 
images_folder = "images_test"

# B_changed to funckja zmiennego b_true[1]
def simulation2(t, b_true, B_changed, Lambda):
    N = len(t)
    P_k = np.array([[100, 0, 0],
                    [0, 100, 0],
                    [0, 0, 100]])

    b_estimated = np.zeros((3,N))
    
    V_estimated = np.zeros(N)
    y_estimated = np.zeros(N)

    V_true = np.zeros(N) # prawdziwe wyjście z obiektu bez zakłócenia
    y_true = np.zeros(N) # prawdziwe wyjście z zakłóceniem

    # Tworzenie zakłócenia
    noise = [C *(random.random() + random.random() - 1) for _ in range(N)]
    # Tworzenie danych przed pętlą 
    # Dla [0]
    v_wanted = (np.sin(2*np.pi/3 * 0) + 1.5)
    u_calculated = np.zeros(N)
    u_calculated[0] = v_wanted
    Phi = np.array([[u_calculated[0]],
                    [0],
                    [0]])
    b_true[1] = B_changed[0]
    V_true[0] = b_true[0]*u_calculated[0]
    y_true[0] = V_true[0]  + noise[0]
    new_P_k = 1/Lambda * (P_k - (np.dot(np.dot(np.dot(P_k,Phi),Phi.T),P_k))/ (Lambda + np.dot(np.dot(Phi.T, P_k),Phi)))
    P_k = new_P_k

    B_estimated = [ [0],
                    [0],
                    [0]]
    b_estimated[:,0] = (B_estimated + (y_true[0] - np.dot(Phi.T, B_estimated)) * np.dot(P_k,Phi)).reshape((3,)) 

    # DLa [1]
    v_wanted = (np.sin(2*np.pi/3 * 1) + 1.5)
    u_calculated[1] = v_wanted/b_estimated[0, 0]
    Phi = np.array([[u_calculated[1]],
                    [u_calculated[0]],
                    [0]])
    b_true[1] = B_changed[1]
    V_true[1] = b_true[0]*u_calculated[1] + b_true[1]*u_calculated[0] 
    y_true[1] =  V_true[1] + noise[1]
    new_P_k = 1/Lambda * (P_k - (np.dot(np.dot(np.dot(P_k,Phi),Phi.T),P_k))/ (Lambda + np.dot(np.dot(Phi.T, P_k),Phi)))
    P_k = new_P_k

    B_estimated = [ [b_estimated[0, 0]],
                    [b_estimated[1, 0]],
                    [b_estimated[2, 0]]]
    b_estimated[:,1] = (B_estimated + (y_true[1] - np.dot(Phi.T, B_estimated)) * np.dot(P_k,Phi)).reshape((3,)) 

    for k in range(2, N):
        # Do zmiany b* 
        b_true[1] = B_changed[k]
            
        # Dla sygnału trójkatnego:
        # v_wanted = 
        v_wanted = (np.sin(2*np.pi/3 * k) + 1.5)
        u_calculated[k] = (v_wanted -(b_estimated[1, k-1]* u_calculated[k-1] + b_estimated[2, k-1]*u_calculated[k-2]))/b_estimated[0, k-1]
        Phi = np.array([[u_calculated[k]],
                        [u_calculated[k-1]],
                        [u_calculated[k-2]]])

        # Wyliczamy nowe wyjście na podstawie oczekiwanego wejścia?? z b_true
        V_true[k] =  (b_true[0]*u_calculated[k] + b_true[1]*u_calculated[k-1] + b_true[2]*u_calculated[k-2])
        y_true[k] = V_true[k] + noise[k]

        # Calculate P_k - macierz kowariancji P_k to P(k-1) a new_P_k to P(k)
        new_P_k = 1/Lambda * (P_k - (np.dot(np.dot(np.dot(P_k,Phi),Phi.T),P_k))/ (Lambda + np.dot(np.dot(Phi.T, P_k),Phi)))
        P_k = new_P_k

        # Calculate b_estimated 
        B_estimated = [[b_estimated[0, k-1]],
                       [b_estimated[1, k-1]],
                       [b_estimated[2, k-1]]]
        b_estimated[:,k] = (B_estimated + (y_true[k] - np.dot(Phi.T, B_estimated)) * np.dot(P_k,Phi)).reshape((3,)) 
            
        V_estimated[k] =  (b_estimated[0, k]*u_calculated[k] + b_estimated[1, k]*u_calculated[k-1] + b_estimated[2, k]*u_calculated[k-2])
        y_estimated[k] = V_estimated[k] + noise[k]

    # print(f"B true = {B_true}")
    print(f"B2 = {b_estimated[:,49]}")    
    return V_true, V_estimated, y_true, y_estimated, b_estimated

def image2(t, b_true, B_changed, Lambda):
    V_true, V_estimated, y_true, y_estimated, b_estimated= simulation2(t, b_true, B_changed, Lambda)
    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(111)
    ax.plot(t, V_true, c='b', label="Fala na wyjściu -> prawdziwa") 
    ax.plot(t, V_estimated, c='r', label="Estymowana fala")
    ax.scatter(t, V_estimated, c='r', marker="o", s=10) 
    # ax.plot(t, y_true, c='g', label="Fala na wyjściu + szum -> prawdziwa")
    # ax.plot(t, y_estimated, c='r', label="Estymowana fala + szum")  
    # ax.scatter(t, y_estimated, c='r', marker="o", s=10, label="Estymowana fala + szum")  
    ax.set_title(f'Prawdziwa i estymowana fala bez szumu przy zmiennym w czasie b* dla Lamby = {Lambda}')
    ax.legend(loc='upper right')
    ax.set_xlabel('Czas (s)')
    ax.set_ylabel('Amplituda')
    fig.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"Fala_zmienne_b={Lambda}.png"))

    
    fig_est = plt.figure(figsize=(14, 6))
    ax_est = fig_est.add_subplot(111)
    ax_est.scatter(t, b_estimated[0], c='r', marker="o", s=10, label="Estymowane b0 od Lambdy")  
    ax_est.plot(t, [b_true[0] for _ in range(len(t))], c='black') 
    ax_est.scatter(t, b_estimated[1], c='b', marker="o", s=10, label="Estymowane b1 od Lambdy")
    ax_est.plot(t, B_changed, c='black') 
    ax_est.scatter(t, b_estimated[2], c='g', marker="o", s=10, label="Estymowane b2 od Lambdy") 
    ax_est.plot(t, [b_true[2] for _ in range(len(t))], c='black') 
    ax_est.set_title(f'Estymator b^  przy zmiennym w czasie b* dla Lambdy = {Lambda}')
    # ax_est.legend(loc='')
    ax_est.set_xlabel('Czas (s)')
    ax_est.set_ylabel('Amplituda')
    ax_est.grid(True)
    # ax_est.set_ylim(0, 5)
    fig_est.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"B_estymowane_zmienne={Lambda}.png"))


def simulation(N, b_true, Lambda):    
    P_k = np.array([[100, 0, 0],
                    [0, 100, 0],
                    [0, 0, 100]])
    
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
        V_true[k] = np.dot(Phi.T, b_true)
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
    

def image(t, b_true, Lambda):
    V_true, V_estimated, y_true, y_estimated, b_estimated = simulation(len(t), b_true, Lambda)
    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(111)
    ax.plot(t, V_true, c='b', label="Fala na wyjściu -> prawdziwa") 
    ax.plot(t, V_estimated, c='r', label="Estymowana fala")
    ax.scatter(t, V_estimated, c='r', marker="o", s=10) 
    # ax.plot(t, y_true, c='g', label="Fala na wyjściu + szum -> prawdziwa")
    # ax.plot(t, y_estimated, c='r', label="Estymowana fala + szum")  
    # ax.scatter(t, y_estimated, c='r', marker="o", s=10, label="Estymowana fala + szum")  
    ax.set_title(f'Prawdziwa i estymowana fala bez szumu dla Lamby = {Lambda}')
    ax.legend(loc='upper right')
    ax.set_xlabel('Czas (s)')
    ax.set_ylabel('Amplituda')
    fig.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"Estymowana_Lambda={Lambda}.png"))

    
    fig_est = plt.figure(figsize=(14, 6))
    ax_est = fig_est.add_subplot(111)
    ax_est.plot(t, b_estimated[0], c='r', label="Estymowane b0 od Lambdy")  #marker="o", s=10,
    ax_est.plot(t, [b_true[0] for _ in range(len(t))], c='black') 
    ax_est.plot(t, b_estimated[1], c='b', label="Estymowane b1 od Lambdy")
    ax_est.plot(t, [b_true[1] for _ in range(len(t))], c='black') 
    ax_est.plot(t, b_estimated[2], c='g', label="Estymowane b2 od Lambdy") 
    ax_est.plot(t, [b_true[2] for _ in range(len(t))], c='black') 
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
    N = 200 # Amount of samples
    t = np.linspace(0, duration, N, endpoint=False) # <class 'numpy.ndarray'>
    # u_k = np.random.uniform(0, 3,  N)
    Lambda = [1, 0.99, 0.95, 0.9, 0.8]
    b_true = [1, 1, 1]
    
    B_true = ((4 * amplitude) / period) * np.abs(((t - (period * 0.25))%period) - (period * 0.5)) - amplitude + b_true[1]

    # Part I
    image(t, b_true, Lambda[0])

    # Part II
    # for i in range(len(Lambda)):
    #     image2(t, b_true, B_true, Lambda[i])
    
if __name__ == "__main__":
    main()

