import matplotlib.pyplot as plt
import numpy as np
import random
import os
from matplotlib import cm

C = 0.5 
images_folder = "images_part_2"
img_mse = "images_mse"


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

    previous_b_est = [[0],
                      [0],
                      [0]]

    for k in range(N):
        # Wyliczamy nowe wyjście na podstawie oczekiwanego wejścia?? z b_true
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
            
        V_estimated[k] = np.dot(Phi.T, b_estimated[:,k])
        y_estimated[k] = V_estimated[k] + noise[k]
        if k < N - 1:
                Phi[2,0] = Phi[1,0]
                Phi[1,0] = Phi[0,0]
                Phi[0,0] = u_k[k+1]
                    
    return b_estimated
    
def MSE(t, b_true, b_estimated, Lambda):
    MSE_b0 = [0.0 for i in  range(len(t))]
    # MSE_b1 = [0.0 for i in  range(len(t))]
    # MSE_b2 = [0.0 for i in  range(len(t))]
    mse = 0
    for i in range(len(t)):
        MSE_b0[i] = (b_true[0, i] - b_estimated[0, i])**2
        # MSE_b1[i] = (b_true[1, i] - b_estimated[1, i])**2
        # MSE_b2[i] = (b_true[2, i] - b_estimated[2, i])**2
        if i >= 40: 
            mse += MSE_b0[i]
    fig = plt.figure(figsize=(14, 6))
    ax_est = fig.add_subplot(111)
    ax_est.plot(t, MSE_b0, c='r', label="MSE dla b0")  
    # ax_est.plot(t, MSE_b1, c='b', label="MSE dla b1")
    # ax_est.plot(t, MSE_b2, c='g', label="MSE dla b2")
    # ax_est.legend(loc='best', bbox_to_anchor=(1.12, 0.55), borderaxespad=0.0) 
    ax_est.set_xlabel('Liczba próbek')
    ax_est.set_ylabel('MSE estymatora b0')
    ax_est.grid(True)
    ax_est.set_ylim(0, 0.1)
    fig.savefig(os.path.join(os.path.dirname(__file__), img_mse, f"MSE_lambda={Lambda}.png"))
    return mse/(len(t) - 40)
     
def zad2(t, b_true, Lambda):
    b_estimated = simulation(len(t), b_true, Lambda)
    
    mse = MSE(t, b_true, b_estimated, Lambda)

    fig_est = plt.figure(figsize=(14, 6))
    ax_est = fig_est.add_subplot(111)
    ax_est.plot(t, b_estimated[0], c='r', label="b0")  #marker="o", s=10,
    ax_est.plot(t, b_true[0], c='black') 
    ax_est.plot(t, b_estimated[1], c='b', label="b1")
    ax_est.plot(t, b_true[1], c='black') 
    ax_est.plot(t, b_estimated[2], c='g', label="b2") 
    ax_est.plot(t, b_true[2], c='black') 
    ax_est.legend(loc='best', bbox_to_anchor=(1.1, 0.55), borderaxespad=0.0)
    ax_est.set_xlabel('Liczba próbek')
    ax_est.set_ylabel('Wartości estymotorów')
    ax_est.grid(True)
    fig_est.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"B_estymowane_lambda={Lambda}.png"))
    return mse

def main():
    duration = 1000.0  # Duration of the u_k(seconds)
    N = int(duration)# Amount of samples
    t = np.linspace(0, duration, N, endpoint=False) # <class 'numpy.ndarray'>

    Lambda = [0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.9, 0.85, 0.8, 0.7, 0.6]

    param0 = [1.0 for _ in range(len(t))]
    param1 = [2.0 for _ in range(len(t))]
    param2 = [3.0 for _ in range(len(t))]
    b_true =  np.array([param0, param1, param2])
# =================================================================================
    amplituda = 0.1
    period = 200

    czas = np.linspace(0, duration, N, endpoint=False)
    fala_trojkatna = ((4 * amplituda) / period) * np.abs(((czas - (period * 0.25))%period) - (period * 0.5)) - amplituda + 1

    b_true[0] = fala_trojkatna
# ================================================================================
    # zad2(t, b_true, 1)
    mse = np.zeros(len(Lambda))
    mse_min = 1
    for i in range(len(Lambda)):
        mse[i] = zad2(t, b_true, Lambda[i])
        if mse[i] < mse_min:
            mse_min = mse[i]
            llambda = Lambda[i]
    print(f"Mse min = {mse_min} dla lambdy = {llambda}")
    
if __name__ == "__main__":
    main()