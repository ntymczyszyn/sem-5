import matplotlib.pyplot as plt
import numpy as np
import random
import os
from matplotlib import cm

C = 0.7

def preparing_true_data(u_k, t, b_true):
    N = len(t)
    V_true = np.zeros(N)
    y_true = np.zeros(N)
    noise = np.zeros(N)
    for k in range(2, N):
        noise[k] = C *(random.random() + random.random() - 1)
        V_true[k] =  (b_true[0]*u_k[k] + b_true[1]*u_k[k-1] + b_true[2]*u_k[k-2])
        y_true[k] = V_true[k] + noise[k]
    return y_true, V_true, noise

def simulation(u_k, t,  b_true, Lambda):
    N = len(t)
    y_k, V_true, noise = preparing_true_data(u_k, t, b_true)
    
    P_k = np.array([[100, 0, 0],
                    [0, 100, 0],
                    [0, 0, 100]])

    b_est0 = np.zeros(N)
    b_est1 = np.zeros(N)
    b_est2 = np.zeros(N)
    b_estimated = np.zeros((3,N))
    # b_estimated = np.array([[b_est0[0]],
    #                         [b_est1[0]],
    #                         [b_est2[0]]])
    
    V_k = np.zeros(N)
    y_k_estimated = np.zeros(N)
    y_k_estimated = y_k
    MSE_sum = 0
    MSE_sum2 = 0
    for k in range(3, N):
        Phi = np.array([[u_k[k]],
                        [u_k[k-1]],
                        [u_k[k-2]]])

        # Calculate P_k - macierz kowariancji P_k to P(k-1) a new_P_k to P(k)
        new_P_k = 1/Lambda * (P_k - (np.dot(np.dot(np.dot(P_k,Phi),Phi.T),P_k))/ (Lambda + np.dot(np.dot(Phi.T, P_k),Phi)))
        P_k = new_P_k

        # Wyliczamy ze starym b nowe wyjście
        
        # Calculate b_estimated 
        B_estimated = [[b_estimated[0, k-1]],
                       [b_estimated[1, k-1]],
                       [b_estimated[2, k-1]]]
        b_estimated[:,k] = (B_estimated + (y_k[k] - np.dot(Phi.T, B_estimated)) * np.dot(P_k,Phi)).reshape((3,)) 

        V_k[k] =  (b_estimated[0][k]*u_k[k] + b_estimated[1][k]*u_k[k-1] + b_estimated[2][k]*u_k[k-2])
        y_k_estimated[k] = V_k[k] + noise[k]
        b_est0[k] = b_estimated[0][k]
        b_est1[k] = b_estimated[1][k]
        b_est2[k] = b_estimated[2][k]
        # V_k[k] =  (b_est0[k]*u_k[k] + b_est1[k]*u_k[k-1] + b_est2[k]*u_k[k-2])
        # y_k_estimated[k] = V_k[k] + noise[k]

        MSE_sum += (np.abs(V_k[k] - V_true[k]))**2
        MSE_sum2 += (np.abs(y_k_estimated[k] - y_k[k]))**2


    MSE = MSE_sum/(N-2)
    MSE2 = MSE_sum2/(N-2)
    print(f"MSE dla Lambdy = {Lambda} : {MSE}")
    print(f"MSE2 dla Lambdy = {Lambda} : {MSE2}")
    return V_k, V_true, y_k_estimated, y_k, b_est0, b_est1, b_est2
    

def image(t, u_k, b_true, Lambda):
    V_k, V_true, estimated_with_noise, y_k, b_est0, b_est1, b_est2 = simulation(u_k, t,  b_true, Lambda)
    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(111)
    ax.plot(t, V_k, c='b', label="Estymowana fala") 
    ax.plot(t, V_true, c='r', label="Fala trójkątna bez szumu")
    ax.scatter(t, V_k, c='b', marker="o", s=10, label="Estymowana fala") 
    # ax.scatter(t, V_true, c='r', marker="o", s=10, label="Fala trójkątna bez szumu")
    # ax.scatter(t, estimated_with_noise, c='r', marker="o", s=10, label="Estymowana fala + szum")  
    # ax.scatter(t, y_k, c='g', marker="o", s=10, label="Zaszumiona fala trójkątna")
    # ax.plot(t, estimated_with_noise, c='r', label="Estymowana fala + szum")  
    # ax.plot(t, y_k, c='g', label="Zaszumiona fala trójkątna")
    ax.set_title(f'Estymowana i zaszumiona fala dla Lamby = {Lambda}')
    ax.legend(loc='upper right')
    ax.set_xlabel('Czas (s)')
    ax.set_ylabel('Amplituda')
    fig.savefig(os.path.join(os.path.dirname(__file__), "images_test", f"Estymowana_Lambda={Lambda}.png"))

    
    fig_est = plt.figure(figsize=(14, 6))
    ax_est = fig_est.add_subplot(111)
    ax_est.scatter(t, b_est0, c='r', marker="o", s=10, label="Estymowane b0 od Lambdy")  
    ax_est.plot(t, [b_true[0] for i in range(len(t))], c='black') 
    ax_est.scatter(t, b_est1, c='b', marker="o", s=10, label="Estymowane b1 od Lambdy")
    ax_est.plot(t, [b_true[1] for i in range(len(t))], c='black') 
    ax_est.scatter(t, b_est2, c='g', marker="o", s=10, label="Estymowane b2 od Lambdy") 
    ax_est.plot(t, [b_true[2] for i in range(len(t))], c='black') 
    ax_est.set_title(f'Estymowana i zaszumiona fala dla Lamby = {Lambda}')
    # ax_est.legend(loc='')
    ax_est.set_xlabel('Czas (s)')
    ax_est.set_ylabel('Amplituda')
    ax_est.grid(True)
    # ax_est.set_ylim(0, 5)
    fig_est.savefig(os.path.join(os.path.dirname(__file__), "images_test", f"B_estymowane_lambda={Lambda}.png"))


# ZNANE
# u_k
# -> u_k -- wartość na wejściu 
# y_k -> y_3 -- wartość na wyjściu
# SZUKANE
# b_true -> poprzez b_estimated
# INNE
# V_k -> sygnał po wyjściu z obiektu, którym mamy "sterować" 
def main():
    duration = 1000.0  # Duration of the u_k(seconds)
    N = 50
    t = np.linspace(0, duration, N, endpoint=False) # <class 'numpy.ndarray'>
    u_k = np.random.uniform(0, 3,  N)
    #u_k = [ random.random()-0.5 for _ in range(N)]
    # u_k = [1 for i in range(len(t))]

    Lambda = [1]
    b_0, b_1, b_2 = 2, 3, 1 #17.5, 10, 2.5
    b_true = [b_0, b_1, b_2]
    
    for i in range(len(Lambda)):
        image(t, u_k, b_true, Lambda[i])

    # image_MSE(t, u_k, b_true, Lambda)
    
if __name__ == "__main__":
    main()

