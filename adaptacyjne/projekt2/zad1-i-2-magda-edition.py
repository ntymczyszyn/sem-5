import matplotlib.pyplot as plt
import numpy as np
import random
import os
from matplotlib import cm

C = 0.5 # 
images_folder = "sterowanie"

# B_changed to funckja zmiennego b_true[1]
def simulation(N, b_true, Lambda, v_wanted):
    P_k = np.array([[100, 0, 0],
                    [0, 100, 0],
                    [0, 0, 100]])
    
    b_estimated = np.zeros((3,N))
    b_estimated[0, 0] = 1
    b_estimated[1, 0] = 1
    b_estimated[2, 0] = 1

    V_estimated = np.zeros(N)
    y_estimated = np.zeros(N)
    V_true = np.zeros(N) # prawdziwe wyjście z obiektu bez zakłócenia
    y_true = np.zeros(N) # prawdziwe wyjście z zakłóceniem
    u_k = np.zeros(N)
    u_k[0] = v_wanted[0]/b_estimated[0,0]
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
        V_true[k] = np.dot(Phi.T, b_true[:,k])[0]
        y_true[k] = V_true[k] + noise[k]

        # Calculate P_k - macierz kowariancji P_k to P(k-1) a new_P_k to P(k)
        P_k = 1/Lambda * (P_k - (np.dot(np.dot(np.dot(P_k,Phi),Phi.T),P_k))/ (Lambda + np.dot(np.dot(Phi.T, P_k),Phi)))

        # Calculate b_estimated 
        if k > 0:
            previous_b_est = [[b_estimated[0, k-1]],
                              [b_estimated[1, k-1]],
                              [b_estimated[2, k-1]]]
            b_estimated[:,k] = (previous_b_est + (y_true[k] - np.dot(Phi.T, previous_b_est)) * np.dot(P_k,Phi)).reshape((3,)) 
            
        V_estimated[k] = np.dot(Phi.T, b_estimated[:,k])[0]
        y_estimated[k] = V_estimated[k] + noise[k]

        # sterowanie
        if k == 0:
            u_k[k+1] = (v_wanted[k+1] - b_estimated[1,k]*u_k[k])/b_estimated[0,k]
            print(f"u_k dla 1 = {u_k[1]}")
        elif k < N - 1:
            u_k[k+1] = (v_wanted[k+1] - b_estimated[1,k]*u_k[k] - b_estimated[2,k]*u_k[k-1])/b_estimated[0,k]

        if k < N - 1:
                Phi[2,0] = Phi[1,0]
                Phi[1,0] = Phi[0,0]
                Phi[0,0] = u_k[k+1]
                    
    return V_true, V_estimated, y_true, y_estimated, b_estimated
    

def image(t, b_true, Lambda, v_wanted):
    V_true, V_estimated, y_true, y_estimated, b_estimated= simulation(len(t), b_true, Lambda, v_wanted)
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
    fig.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"Sterowanie_fala_L={Lambda}.png"))

    
    fig_est = plt.figure(figsize=(14, 6))
    ax_est = fig_est.add_subplot(111)
    ax_est.scatter(t, b_estimated[0], c='r', marker="o", s=10, label="Estymowane b0 od Lambdy")  
    ax_est.plot(t, b_true[0], c='black') 
    ax_est.scatter(t, b_estimated[1], c='b', marker="o", s=10, label="Estymowane b1 od Lambdy")
    ax_est.plot(t, b_true[1], c='black') 
    ax_est.scatter(t, b_estimated[2], c='g', marker="o", s=10, label="Estymowane b2 od Lambdy") 
    ax_est.plot(t, b_true[2], c='black') 
    ax_est.set_title(f'Estymator b^  przy zmiennym w czasie b* dla Lambdy = {Lambda}')
    # ax_est.legend(loc='')
    ax_est.set_xlabel('Czas (s)')
    ax_est.set_ylabel('Amplituda')
    ax_est.grid(True)
    # ax_est.set_ylim(0, 5)
    fig_est.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"Sterowanie_B_L={Lambda}.png"))


def simulation2(N, b_true, Lambda, v_wanted):
    P_k = np.array([[100, 0, 0],
                    [0, 100, 0],
                    [0, 0, 100]])

    b_estimated = np.zeros((3,N))
    
    b_estimated[0,0] = 1
    b_estimated[1,0] = 1
    b_estimated[2,0] = 1

    V_estimated = np.zeros(N)
    y_estimated = np.zeros(N)

    V_true = np.zeros(N) # prawdziwe wyjście z obiektu bez zakłócenia
    y_true = np.zeros(N) # prawdziwe wyjście z zakłóceniem

    # Tworzenie zakłócenia
    noise = [C *(random.random() + random.random() - 1) for _ in range(N)]
    # Tworzenie danych przed pętlą 
    # Dla [0]
    u_calculated = np.zeros(N)
    u_calculated[0] = (v_wanted[0])/b_estimated[0, 0]
    Phi = np.array([[u_calculated[0]],
                    [0],
                    [0]])
    V_true[0] = np.dot(Phi.T, b_true[:,0])
    y_true[0] = V_true[0]  + noise[0]
    new_P_k = 1/Lambda * (P_k - (np.dot(np.dot(np.dot(P_k,Phi),Phi.T),P_k))/ (Lambda + np.dot(np.dot(Phi.T, P_k),Phi)))
    P_k = new_P_k

    previous_estimate = [ [0],
                    [0],
                    [0]]
    b_estimated[:,0] = (previous_estimate + (y_true[0] - np.dot(Phi.T, previous_estimate)) * np.dot(P_k,Phi)).reshape((3,)) 

    # DLa [1]
    u_calculated[1] = ((v_wanted[1]) - (b_estimated[1, 0]* u_calculated[0]))/b_estimated[0, 0]
    Phi = np.array([[u_calculated[1]],
                    [u_calculated[0]],
                    [0]])

    V_true[1] = np.dot(Phi.T, b_true[:,1]) 
    y_true[1] =  V_true[1] + noise[1]
    new_P_k = 1/Lambda * (P_k - (np.dot(np.dot(np.dot(P_k,Phi),Phi.T),P_k))/ (Lambda + np.dot(np.dot(Phi.T, P_k),Phi)))
    P_k = new_P_k

    previous_estimate = [ [b_estimated[0, 0]],
                    [b_estimated[1, 0]],
                    [b_estimated[2, 0]]]
    b_estimated[:,1] = (previous_estimate + (y_true[1] - np.dot(Phi.T, previous_estimate)) * np.dot(P_k,Phi)).reshape((3,)) 

    for k in range(2, N):
        # Tworzenie u_k  
        u_calculated[k] = ((v_wanted[k]) -  (b_estimated[1, k-1]* u_calculated[k-1] + b_estimated[2, k-1]*u_calculated[k-2]))/b_estimated[0, k-1]
        Phi = np.array([[u_calculated[k]],
                        [u_calculated[k-1]],
                        [u_calculated[k-2]]])

        # Wyliczamy nowe wyjście na podstawie oczekiwanego wejścia?? z b_true
        V_true[k] = np.dot(Phi.T, b_true[:,k])
        y_true[k] = V_true[k] + noise[k]

        # Calculate P_k - macierz kowariancji P_k to P(k-1) a new_P_k to P(k)
        P_k = 1/Lambda * (P_k - (np.dot(np.dot(np.dot(P_k,Phi),Phi.T),P_k))/ (Lambda + np.dot(np.dot(Phi.T, P_k),Phi)))

        # Calculate b_estimated 
        previous_estimate = [[b_estimated[0, k-1]],
                       [b_estimated[1, k-1]],
                       [b_estimated[2, k-1]]]
        b_estimated[:,k] = (previous_estimate + (y_true[k] - np.dot(Phi.T, previous_estimate)) * np.dot(P_k,Phi)).reshape((3,)) 
            
        V_estimated[k] =  np.dot(Phi.T, b_estimated[:,k])
        y_estimated[k] = V_estimated[k] + noise[k]

    print(f"Dla 50 : b_est = {b_estimated[1,50]}, u_cal = {u_calculated[50]}, miltiply = :{b_estimated[1,50] * u_calculated[50]}")
    print(f"B2 = {b_estimated[:,450]}")    
    return V_true, V_estimated, y_true, y_estimated, b_estimated

def image2(t, b_true, Lambda, v_wanted):
    V_true, V_estimated, y_true, y_estimated, b_estimated = simulation2(len(t), b_true, Lambda, v_wanted)
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
    fig.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"Ster_fala_L={Lambda}.png"))

    
    fig_est = plt.figure(figsize=(14, 6))
    ax_est = fig_est.add_subplot(111)
    ax_est.scatter(t, b_estimated[0], c='r', marker="o", s=10, label="Estymowane b0 od Lambdy")  
    ax_est.plot(t, b_true[0], c='black') 
    ax_est.scatter(t, b_estimated[1], c='b', marker="o", s=10, label="Estymowane b1 od Lambdy")
    ax_est.plot(t, b_true[1], c='black') 
    ax_est.scatter(t, b_estimated[2], c='g', marker="o", s=10, label="Estymowane b2 od Lambdy") 
    ax_est.plot(t, b_true[2], c='black') 
    ax_est.set_title(f'Estymator b^  przy zmiennym w czasie b* dla Lambdy = {Lambda}')
    # ax_est.legend(loc='')
    ax_est.set_xlabel('Czas (s)')
    ax_est.set_ylabel('Amplituda')
    ax_est.grid(True)
    # ax_est.set_ylim(0, 5)
    fig_est.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"Ster_b_L={Lambda}.png"))

def main():
    duration = 300.0  # Duration of the u_k(seconds)
    N = int(duration)# Amount of samples
    t = np.linspace(0, duration, N, endpoint=False) # <class 'numpy.ndarray'>


    param0 = [1.0 for _ in range(len(t))]
    param1 = [6.0 for _ in range(len(t))]
    param2 = [11.0 for _ in range(len(t))]
    b_true =  np.array([param0, param1, param2])
# =================================================================================
    amplituda = 0.1
    period = 100

    czas = np.linspace(0, duration, N, endpoint=False)
    fala_trojkatna = ((4 * amplituda) / period) * np.abs(((czas - (period * 0.25))%period) - (period * 0.5)) - amplituda + 1
    
    period = 50
    amplituda = 2
    fala_trojkatna2 = ((4 * amplituda) / period) * np.abs(((czas - (period * 0.25))%period) - (period * 0.5)) - amplituda + 1

    b_true[0] = fala_trojkatna
# ================================================================================
    # zad2(t, b_true, 1)
    # mse = np.zeros(len(Lambda))
    # mse_min = 1
    Lambda = [0.98, 0.91]   # [0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.9, 0.85, 0.8, 0.7, 0.6]

    for i in range(len(Lambda)):
        # mse[i] = image(t, b_true, Lambda[i], fala_trojkatna2)
        image(t, b_true, Lambda[i], fala_trojkatna2)
        # if mse[i] < mse_min:
        #     mse_min = mse[i]
        #     llambda = Lambda[i]
    # print(f"Mse min = {mse_min} dla lambdy = {llambda}")
    
if __name__ == "__main__":
    main()

