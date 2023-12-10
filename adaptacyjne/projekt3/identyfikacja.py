import matplotlib.pyplot as plt
import numpy as np
import random
import os

C = 0
images_folder = "images"
# images_folder2 = "images"

def simulation(N):
    u_1 = [random.random() for _ in range(N)]
    u_2 = [random.random() for _ in range(N)]
    z_1 = [C *(random.random() + random.random() - 1) for _ in range(N)]
    z_2 = [C *(random.random() + random.random() - 1) for _ in range(N)]
    a_1, a_2 = 1/2, 1.4
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
        if k > 0:  # tutaj bierzemy dla kolejnego?
            X[:,k] = np.dot(H, Y[:,k-1])
    return U, Y, X, H, I

def estimation(N):
    U, Y, X, H, I = simulation(N)
    W = np.array([[U[0], X[0]],[U[1], X[1]]])
    W_1 = np.array([U[0], X[0]]) # for block 1
    W_2 = np.array([U[1], X[1]]) # for block 2
    EST = np.zeros((2,N,2))
    EST_1 = np.zeros((N,2))
    EST_2 = np.zeros((N,2))
    sum1 = 0
    for i in range(2):
        for k in range(N):
            EST[i,k] = np.dot(np.dot(Y[i,k], W[i,:,k].T), np.dot(W[i,:,k], W[i,:,k].T))
        print(f"Dla i = {i} \n EST = {EST[i]} \n")
    for k in range(N):
        EST_1[k] = np.dot(np.dot(Y[0,k], W_1[:,k].T), np.dot(W_1[:,k], W_1[:,k].T))
        EST_2[k] = np.dot(np.dot(Y[1,k], W_2[:,k].T), np.dot(W_2[:,k], W_2[:,k].T))
        sum1 += EST_1[k,0]
        print(f" Est1 = {round(EST_1[k,0],6)} \nEST2 = {round(EST_2[k,0],6)}")
    print(f"Srednia : {sum1/N} \nOczekiwana : {1/2}")
    a = [[EST_1[N-1, 0], 0],
         [0, EST_2[N-1, 0]]]
    b = [[EST_1[N-1,1], 0],
         [0, EST_2[N-1,1]]]
    return U, Y, X, H, I, a, b

def optimalization(N):
     U, Y, X, H, I, A, B = estimation(N)
     # Ograniczenia u1, u2 <= 1
     u_1 = np.linspace(0, 1, 5)
     u_2 = np.linspace(0, 1, 5)
     for i in range(len(u_1)):
        min = 5
        for j in range(len(u_1)):
             u = np.array([[u_1[i]],
                           [u_2[j]]])
             y = np.dot((I - np.dot(A, H))**(-1) , np.dot(B, u))
             if(y[1] < min):
                min = y[1]
                index = j
        print(f"Min = {min}, Index = {index}")
     return 0

def main():
    duration = 10.0  # Duration of the u_k(seconds)
    N = int(duration)# Amount of samples
    t = np.linspace(0, duration, N, endpoint=False) # <class 'numpy.ndarray'>
    optimalization(N)



main()