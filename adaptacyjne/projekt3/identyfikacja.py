import matplotlib.pyplot as plt
import numpy as np
import random
import os

C = 0.4
images_folder = "images"
# images_folder2 = "images"

def simulation(N):
    u_1 = [random.random() for _ in range(N)]
    u_2 = [random.random() for _ in range(N)]
    z_1 = [C *(random.random() + random.random() - 1) for _ in range(N)]
    z_2 = [C *(random.random() + random.random() - 1) for _ in range(N)]
    a_1, a_2 = 1/2, 1/4
    b_1, b_2= 1, 1
    U =  np.array([u_1, u_2])
    Z =  np.array([z_1, z_2])
    A =  np.array([[a_1, 0],
                   [0, a_2]])
    B =  np.array([[b_1, 0],
                   [0, b_2]])
    H =  np.array([[0, 1],
                   [1, 0]])
    I =  np.array([[1, 0],
                   [0, 1]])
    Y =  np.zeros((2,N))
    X =  np.zeros((2,N))
    for k in range(N):
        Y[:,k] = np.dot((I - np.dot(A, H))**(-1) , np.dot(B, U[:,k])) + np.dot((I - np.dot(A, H))**(-1), Z[:,k])
        # if k > 0:  # tutaj bierzemy dla kolejnego?
        X[:,k] = np.dot(H, Y[:,k])
    return U, Y, X, H, I

def identification(t):
    N = len(t)
    U, Y, X, H, I = simulation(N)
    W = np.array([[U[0], X[0]],
                  [U[1], X[1]]])
    W_1 = np.array([U[0], X[0]]) # for block 1
    W_2 = np.array([U[1], X[1]]) # for block 2
    EST = np.zeros((2,2))
    for i in range(2):
        EST[i] = np.dot(np.dot(Y[i], W[i].T), (np.dot(W[i], W[i].T)**(-1)))
        print(f'Przed potega: {np.dot(W[i], W[i].T)}\nPotega -1 : {(np.dot(W[i], W[i].T)**(-1))}') # nie mam pojecia jak powinna wygladać odwrotność
    a = [[EST[0,0], 0],
         [0, EST[1,0]]]
    b = [[EST[0,1], 0],
         [0, EST[1,1]]]
    print(f'a i b = {EST}')
    return U, Y, X, H, I, a, b

def optimalization(t, wanted_output):
    N = len(t)
    U, Y, X, H, I, A, B = identification(t)
    figure_identyfication(t, U, Y, X)

    # Ograniczenia u1, u2 <= 1
    u_1 = np.linspace(0, 1, len(t))
    u_2 = np.linspace(0, 1, len(t))
    Q = np.zeros((len(u_1),len(u_2)))
    y_0_max = 0
    y_1_max = 0
    for i in range(len(u_1)):
        min = 5
        for j in range(len(u_2)):
            u = np.array([[u_1[i]],
                          [u_2[j]]])
            y = np.dot((I - np.dot(A, H))**(-1) , np.dot(B, u))
            if(y[0] > y_0_max):
                y_0_max = y[0]
            if(y[1] > y_1_max):
                y_1_max = y[1]
            Q[i][j] = (y[0] - wanted_output)**2 + (y[1] - wanted_output)**2
    print(f'Y 0 max = {y_0_max}\nY 1 max = {y_1_max}')
    figure_opt(t, u_1, u_2, Q)

def figure_identyfication(t, U, Y, X):
    fig1 = plt.figure(figsize=(12,6))
    ax1 = fig1.add_subplot(1,2,1)
    ax2 = fig1.add_subplot(1,2,2)

    ax1.plot(t, Y[0],  c='b')
    ax1.plot(t, Y[1],  c='orange')

    ax2.plot(t, U[0],  c='b')
    ax2.plot(t, U[1],  c='orange')

    ax1.scatter(t, X[0], c='r')    
    ax1.scatter(t, X[1], c='green')
    #  sprawdzałam czy dobrze idą x i są adekwatnie Y z wcześniejszego przejścia
    fig1.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"Identyfication.png"))


def figure_opt(t, u_1, u_2, Q):
    fig_3d = plt.figure(figsize=(14, 6))
    ax0 = fig_3d.add_subplot(121, projection='3d')
    X, Y = np.meshgrid(u_1, u_2)
    Z = Q
    ax0.plot_surface(X, Y, Z, cmap='viridis')
    ax0.set_xlabel('U_1')
    ax0.set_ylabel('U_2')
    ax0.set_zlabel('Q(U_1, U_2)')
    ax0.set_title('...')

    fig_3d.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"Optimalization.png"))
    return 0

def main():
    duration = 10.0  # Duration of the u_k(seconds)
    N = int(duration)# Amount of samples
    t = np.linspace(0, duration, N, endpoint=False) # <class 'numpy.ndarray'>
    # identification(N)

    optimalization(t, 2)


main()