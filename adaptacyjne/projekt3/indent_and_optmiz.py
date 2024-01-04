import matplotlib.pyplot as plt
import numpy as np
import random
import os

C = 0.5
images_folder = "images"
images_folder2 = "images_n"

a_1, a_2 = 0.5, 0.25 
b_1, b_2 = 1, 1 
A =  np.array([[a_1, 0],
                [0, a_2]]) # parametry A
B =  np.array([[b_1, 0],
                [0, b_2]]) # parametry B
H =  np.array([[0, 1],
                [1, 0]])
I =  np.array([[1, 0],
                [0, 1]])
y_wanted = np.array([[4],
                [4]])

# symulacja sygnału
def simulation(N):
    u_1 = np.random.uniform(0, 3, N)
    u_2 = np.random.uniform(0, 3, N)
    z_1 = [C *(random.random() + random.random() - 1) for _ in range(N)]
    z_2 = [C *(random.random() + random.random() - 1) for _ in range(N)]
    U =  np.array([u_1, u_2]) # wejścia
    Z =  np.array([z_1, z_2]) # zakłócenia
    Y =  np.zeros((2,N))
    X =  np.zeros((2,N))
    for k in range(N):
        Y[:,k] = np.dot(np.dot(np.linalg.inv(I - np.dot(A, H)), B), U[:,k]) + np.dot(np.linalg.inv(I - np.dot(A, H)), Z[:,k])
        X[:,k] = np.dot(H, Y[:,k])

    return U, Y, X

# identyfikacja wartości A i B
def identification(N): 
    U, Y, X = simulation(N)
    W_1 = np.array([X[0], U[0]]) # for block 1 # ZAMIENIONO KOLEJNOŚĆ X i U - DOSTALISMY DOBRA KOLEJNOSC A I B!
    W_2 = np.array([X[1], U[1]]) # for block 2
    EST = np.zeros((2,2)) # pierwsza kolumna to a, druga to b

    EST[0] = np.dot(np.dot(Y[0,:], W_1.T), np.linalg.inv(np.dot(W_1, W_1.T))) # niby wylicza a_1 i b_1
    EST[1] = np.dot(np.dot(Y[1,:], W_2.T), np.linalg.inv(np.dot(W_2, W_2.T)))

    A_est = [[EST[0,0], 0], # czemu te kolumny są zamienione to, totalne idk
         [0, EST[1,0]]]
    B_est = [[EST[0,1], 0],
         [0, EST[1,1]]]
    print(f'a i b = {EST}')
    print(f'a_1 i b_1 = {EST[0]}')
    print(f'a_2 i b_2 = {EST[1]}')

    return U, Y, X, A_est, B_est

#  oczekiwane wartości u bez ograniczeń 
def wanted_input_without_restraints():
    K = np.dot(np.linalg.inv(I - np.dot(A, H)), B)
    u = np.dot(np.linalg.inv(K), y_wanted)
    print(f"U idealne: {u}")
    return u, K

# wyliczanie watrości y od u1 i u2
def Q(u, K):
    u0 = u[0]
    u1 = u[1]
    #1.1429, 0.5714, 0.2857, 1.1429
    y1 = K[0,0] * u0 + K[0,1] * u1
    y2 = K[1,0] * u0 + K[1,1] * u1
    return (y1 - y_wanted[0,0])**2 + (y2 - y_wanted[1,0])**2

# wszykujemy || oczekiwane wartości z ograniczeniami na u1 i u2
#  czy tutaj nie powinno być od wyliczonego A i B ?
def wanted_input_with_restraints_1():
    wanted_point, K = wanted_input_without_restraints()
    u2_values = np.linspace(-1, 1, num=1001) # od -1 do 1.01
    # print(u2_values)
    min_prev = 1000 # wcześniejsze minimum
    point = np.array([0, 0]) # obecnie badany punkta mo

    for u2 in u2_values:
        u1_values = np.linspace(-(np.sqrt(1 - u2**2)), np.sqrt(1 - u2**2), num=1001)
        for u1 in u1_values:
            min_now = Q([u1, u2], K)

            if min_now < min_prev:
                min_prev = min_now
                point = np.array([u1, u2])

    print("Optimal point:", point)
    print("Minimum value:", min_prev)
    return point, wanted_point

    # Funkcja do rysowania okręgu
def draw_circle(center, radius):
    theta = np.linspace(0, 2*np.pi, 100)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    return x, y

def optimisation_plot():
    fig1 = plt.figure(figsize=(12,6))
    circle_x, circle_y = draw_circle((0, 0), 1)
    plt.plot(circle_x, circle_y, label='Okrąg')

    point, wanted_point = wanted_input_with_restraints_1()
    point1 = (0.5, 0.5)  # Czerwona kropka
    point2 = (-0.5, -0.5)  # Niebieska gwiazdka
    x1, y1 = point
    x2, y2 = wanted_point
    plt.scatter(x1, y1, color='red', marker='o', label='Optymalny punkt')
    plt.scatter(x2, y2, color='blue', marker='*', label='Idelany punkt')

    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

    plt.text(*point1, ' Punkt 1', color='red', fontsize=9, verticalalignment='bottom')
    plt.text(*point2, ' Punkt 2', color='blue', fontsize=9, verticalalignment='top')

    plt.axis('equal')
    plt.legend()
    fig1.savefig(os.path.join(os.path.dirname(__file__), images_folder2, f"Optimisation.png"))    


def optimalization(t, wanted_output):
    N = len(t)
    U, Y, X, H, I, A, B = identification(t)
    figure_identification(t, U, Y, X)

    # Ograniczenia u1, u2 <= 1
    u_1 = np.linspace(0, 1, len(t))
    u_2 = np.linspace(0, 1, len(t))
    Q = np.zeros((len(u_1),len(u_2)))
    y_0_max = 0
    y_1_max = 0
    for i in range(len(u_1)):
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

# raczej nie będzie się dało tego zrobić
def parameters_identification_plot(t): #A_est, B_est
    fig1 = plt.figure(figsize=(12,6))
    ax1 = fig1.add_subplot(1,2,1)
    ax2 = fig1.add_subplot(1,2,2)
    a1 = [ a_1 for _ in range(len(t))]
    a2 = [ a_2 for _ in range(len(t))]
    b1 = [ b_1 for _ in range(len(t))]
    b2 = [ b_2 for _ in range(len(t))]
    ax1.plot(t, a1,  c='b')
    ax1.plot(t, a2,  c='b')
    ax2.plot(t, b1,  c='b')
    ax2.plot(t, b2,  c='b')
    # ax1.scatter(t, X[0], c='r')    
    # ax1.scatter(t, X[1], c='green')

    fig1.savefig(os.path.join(os.path.dirname(__file__), images_folder2, f"Identification2.png"))    

def figure_identification(t, U, Y, X):
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
    duration = 100.0  # Duration of the u_k(seconds)
    N = int(duration)# Amount of samples
    t = np.linspace(0, duration, N, endpoint=False) # <class 'numpy.ndarray'>
    # simulation(N)
    identification(N)
    # optymalne wejście (przy braku ograniczeń)
    u_opt_wr = wanted_input_without_restraints()
    
    wanted_input_with_restraints_1()
    optimisation_plot()
    # parameters_identifucation_plot(t)
    #optimalization(t, 2)


main()