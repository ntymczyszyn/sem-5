import matplotlib.pyplot as plt
import numpy as np
import random
import os
import csv

C = 0.5
images_folder = "images"
images_folder2 = "images_n"

duration = 100.0  # Duration of the u_k(seconds)
N = int(duration)# Amount of samples

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

csv_file_path =os.path.join(os.path.dirname(__file__), "images/data.csv")

# symulacja sygnału
def simulation():
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

    return U, Y, X, Z

# identyfikacja wartości A i B
def identification(t): 
    U, Y, X, Z = simulation()
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
    with open(csv_file_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["NEXT:"])
        writer.writerow(["A estymowane", A_est])
        writer.writerow(["B estymowane", B_est])

    ##################################    
    Y_est =  np.zeros((2,N))
    for k in range(N):
        Y_est[:,k] = np.dot(np.dot(np.linalg.inv(I - np.dot(A_est, H)), B_est), U[:,k])
    figure_identification(t, Y, Y_est)
    ##################################
    return A_est, B_est

#  oczekiwane wartości u bez ograniczeń 
def wanted_input_without_restraints():
    K = np.dot(np.linalg.inv(I - np.dot(A, H)), B)
    u = np.dot(np.linalg.inv(K), y_wanted)
    print(f"U idealne: {u}")
    with open(csv_file_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["U idealne", u])
    return u, K

# wyliczanie watrości Y od u1 i u2 
def Q(u, K):
    u0 = u[0]
    u1 = u[1]
    #1.1429, 0.5714, 0.2857, 1.1429
    y1 = K[0,0] * u0 + K[0,1] * u1
    y2 = K[1,0] * u0 + K[1,1] * u1
    return (y1 - y_wanted[0,0])**2 + (y2 - y_wanted[1,0])**2

def optimal_point(A, B, u2 , L, K):
    S = (A+B)/2
    AL = S - L
    BL = S + L
    value_A = Q([AL, u2], K)
    value_B = Q([BL, u2], K)
    min_value = Q([S, u2], K)
    
    if L <= 1/1000:
        return min_value, S
    
    if value_A < value_B:
        min_value, S = optimal_point(A, BL, u2, L = abs(S - A)/2, K = K)
        return min_value, S
    else:
        min_value, S = optimal_point(AL, B, u2, L = abs(S - B)/2, K = K) 
        return min_value, S
        

# wszykujemy || oczekiwane wartości z ograniczeniami na u1 i u2
def wanted_input_with_restraints_1():
    wanted_point, K = wanted_input_without_restraints()
    u2_values = np.linspace(-1, 1, num=1001) # od -1 do 1.01
    # print(u2_values)
    min_prev = 1000 # wcześniejsze minimum
    point = np.array([0, 0]) # obecnie badany punkta mo
    for u2 in u2_values:
        u1_values = np.linspace(-(np.sqrt(1 - u2**2)), np.sqrt(1 - u2**2), num=1001)
        # 
        min_now, S = optimal_point(u1_values[0], u1_values[-1], u2 , 0.5, K)

        if min_now < min_prev:
            min_prev = min_now
            point = np.array([S, u2])

    print("Optimal point:", point)
    print("Minimum value:", min_prev)
    with open(csv_file_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Optimal point:", point])
        writer.writerow(["Minimum value:", min_prev])
        writer.writerow([])
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
    fig1.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"Optimisation.png"))    


def figure_identification(t, Y, Y_est,):
    fig1 = plt.figure(figsize=(12,6))
    ax1 = fig1.add_subplot(1,2,1)
    ax2 = fig1.add_subplot(1,2,2)

    ax1.plot(t, Y[0],  c='r')
    ax1.plot(t, Y_est[0], c='b')
    ax1.set_title("Blok 1", y=0.0)

    ax2.plot(t, Y[1],  c='r')
    ax2.plot(t, Y_est[1], c='b')
    ax2.set_title("Blok 2", y=0.0)
    
    fig1.legend(['Parametry rzeczywiste', 'Parametry estymowane'])
    fig1.suptitle("Sygnał wyjściowy parametrów rzeczywistych oraz estymowanych")

    #  sprawdzałam czy dobrze idą x i są adekwatnie Y z wcześniejszego przejścia
    fig1.savefig(os.path.join(os.path.dirname(__file__), images_folder, f"Identyfication.png"))


def main():
    t = np.linspace(0, duration, N, endpoint=False) # <class 'numpy.ndarray'>
    # simulation(N)
    identification(t)
    
    optimisation_plot()
    # parameters_identifucation_plot(t)
    #optimalization(t, 2)


main()