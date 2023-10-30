import matplotlib.pyplot as plt
import numpy as np
import random
import os
from matplotlib import cm

# number of samples, max h, expected signal 
def calculate_all(N, max, triangular_signal):
    H = [i for i in range(2,max + 2)]
    c = np.linspace(0.05, 1.05, max) 
    var = np.zeros(len(c))
    MSE = np.zeros((len(c), len(H)))
    MSE_opt = np.zeros(len(c))
    H_opt = np.zeros(len(c))
    for current_c in range(len(c)):
        # max value that MSE can be - for finding H opt
        min_MSE = 5    
        var[current_c] = 2*(c[current_c]**2)/3 
        for current_h in range(len(H)):
            noise = [ c[current_c] *(random.random() + random.random() - 1) for _ in range(N)]
            triangular_signal_with_noise = [triangular_signal[i] + noise[i]  for i in range(N)]
            local_sum = np.zeros(N)
            for i in range(N):
                for h in range(H[current_h]):
                    if i > H[current_h]:
                        local_sum[i] += triangular_signal_with_noise[i-h] 
            estimated = np.zeros(N)
            estimated =[ local_sum[i]/(H[current_h]) if (i > H[current_h]) else triangular_signal_with_noise[i]  for i in range(N)]
           
            for i in range(H[current_h], N): # from H till N
                MSE[current_c][current_h] += (estimated[i] - triangular_signal[i])**2
            MSE[current_c][current_h] = MSE[current_c][current_h]/(N - H[current_h])
            # serching for min MSE for each var
            if MSE[current_c][current_h] < min_MSE:
                MSE_opt[current_c] = MSE[current_c][current_h]
                min_MSE = MSE_opt[current_c]
                H_opt[current_c] = H[current_h]      
        
    return H, MSE, var, H_opt, MSE_opt
   
    
def estimate(triangular_signal, N, c, H):
    noise = [ c *(random.random() + random.random() - 1) for _ in range(N)]
    triangular_signal_with_noise = [triangular_signal[i] + noise[i]  for i in range(N)]
    MSE = 0
    local_sum = np.zeros(N)
    for i in range(N):
        for h in range(H):
            if i > H:
                local_sum[i] += triangular_signal_with_noise[i-h] 
    estimated = np.zeros(N)
    estimated =[ local_sum[i]/(H) if (i > H) else triangular_signal_with_noise[i]  for i in range(N)]

    for i in range(H, N): # od H do N
        MSE += (estimated[i] - triangular_signal[i])**2
    MSE = MSE/(N - H)
    return triangular_signal_with_noise, estimated, MSE


def images_MSE(t, N, max, triangular_signal, c_index, H_index):
    H, MSE, var, H_opt, MSE_opt = calculate_all(N, max, triangular_signal)
    # MSE(H) and MSE(var) plots
    fig_H, (ax_H, ax_var) = plt.subplots(1, 2, figsize=(12, 6))
    #  H
    fig_H = plt.figure(figsize=(8, 6))
    ax_H = fig_H.add_subplot(111)
    ax_H.scatter(H, MSE[c_index,:], color='b', marker='o', s=10)
    ax_H.set_title(f'Zależność MSE(H) dla var(Z) ={var[c_index]:.2f}')
    ax_H.set_xlabel('Horyzont pamięci')
    ax_H.set_ylabel('MSE(H)')
    # var
    fig_var = plt.figure(figsize=(8, 6))
    ax_var = fig_var.add_subplot(111)
    ax_var.scatter(var, MSE[: , H_index] , color='r', marker='o', s=10)
    ax_var.set_title(f'Zależność MSE(H) dla H = {H[H_index]} przy różnych wariacjach var(Z)')
    ax_var.set_xlabel('Wariancja')
    ax_var.set_ylabel('MSE(H)')

    # Hopt(var) 
    fig_opt = plt.figure(figsize=(8, 6))
    ax_opt = fig_opt.add_subplot(111)
    ax_opt.scatter(var, H_opt,  c='r', s=10) 
    ax_opt.set_title('Zależność H optymalnego od wariancji var(Z)')
    ax_opt.set_ylabel('Optymalny horyzont pamięci')
    ax_opt.set_xlabel('Wariancja')
    ax_opt.set_ylim(0, max)

    # 3d plot - H, var, MSE(h) + h opt for all calculated var
    fig_3d = plt.figure(figsize=(14, 6))
    ax0 = fig_3d.add_subplot(121, projection='3d')
    ax1 = fig_3d.add_subplot(122, projection='3d')
    X, Y = np.meshgrid(H, var)
    Z = MSE

    # optimal horizon plot
    ax1.scatter(H_opt, var, MSE_opt, c='#fe008b', marker='o', s=40, label="H_opt(var(Z))")
    colors = cm.viridis(Z)
    rcount, ccount, _ = colors.shape
    # change in
    ax0.plot_surface(X, Y, Z, cmap='viridis')
    ax0.set_xlabel('Horyzont pamięci')
    ax0.set_ylabel('Wariancja')
    ax0.set_zlabel('MSE(H)')
    ax0.set_title('MSE(H) przy różnych wariancjach var(Z)')
    ax0.view_init(elev=20, azim=-120)

    surf = ax1.plot_surface(X, Y, Z, rcount=rcount, ccount=ccount, facecolors=colors, shade=False)
    surf.set_facecolor((0,0,0,0))
    ax1.set_xlabel('Horyzont pamięci')
    ax1.set_ylabel('Wariancja')
    ax1.set_zlabel('MSE(H)')
    ax1.set_title('MSE(H) przy różnych wariancjach var(Z)')
    ax1.legend(loc='center left', bbox_to_anchor=(1, 1))
    ax1.view_init(elev=20, azim=-120)
    plt.tight_layout()

    fig_3d.savefig(os.path.join(os.path.dirname(__file__), "images", "Wykres_3d.png"), dpi=500) # APPROVED
    fig_opt.savefig(os.path.join(os.path.dirname(__file__), "images", "Wykres_opt.png"), dpi=500) # APPROVED
    fig_H.savefig(os.path.join(os.path.dirname(__file__), "images", f"Wykres_H_c={var[c_index]:.2f}.png"), dpi=500) # APPROVED
    fig_var.savefig(os.path.join(os.path.dirname(__file__), "images", f"Wykres_var_H={H[H_index]}.png"), dpi=500) # APPROVED

    fig_3d.show()
    g = input("STOP")

# signal w/ and wo/ noise 
def images_signal(t, triangular_signal, N, c_value, H_value, amplitude):
    t_w_n, est, MSE = estimate(triangular_signal, N, c=c_value, H=H_value)
    
    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(121) 
    ax_est = fig.add_subplot(122)
    ax.plot(t, triangular_signal, c='r', label="Prawdziwa fala trójkątna") 
    ax.scatter(t, t_w_n, c='g', marker='o', label="Zaszumiona fala trójkątna")
    var = 2 *(c_value**2)/3
    ax.set_title(f'Prawdziwa i zaszumiona fala trójkątna dla var(Z) = {var:.2f}')
    ax.legend(loc='upper right')
    ax.set_xlabel('Czas (s)')
    ax.set_ylabel('Amplituda')
    ax.set_ylim(-amplitude - c_value - 0.1, amplitude + c_value + 0.1)
    ax_est.plot(t, triangular_signal, c='r', label="Prawdziwa fala trójkątna") 
    ax_est.plot(t[H_value+1:], est[H_value+1:], c='b', marker='o', label="Estymowana fala trójkątna")
    ax_est.set_title(f'Prawdziwa fala trójkątna i jej estymacja dla H = {H_value}')
    ax_est.legend(loc='upper right')
    ax_est.set_xlabel('Czas (s)')
    ax_est.set_ylabel('Amplituda')
    ax_est.set_ylim(-amplitude - c_value - 0.1, amplitude + c_value + 0.1)
    fig.savefig(os.path.join(os.path.dirname(__file__), "estimate", f"Szum_c={c_value}__H={H_value}_MSE={MSE:.3f}.png"), dpi=500) # APPROVED


def main():
    # triangular function parameters 
    frequency = 0.005  # Frequency of the signal (cycles per second)
    period = 1 / frequency
    amplitude = 1.0  # Amplitude of the signal
    duration = 1000.0  # Duration of the signal (seconds)
    sampling_frequency = 0.5 # Sampling frequency (samples per second)
    
    # time vector
    t = np.linspace(0, duration, int(sampling_frequency * duration), endpoint=False) # <class 'numpy.ndarray'>
    N = len(t)
    triangular_signal = ((4 * amplitude) / period) * np.abs(((t - (period * 0.25))%period) - (period * 0.5)) - amplitude
    
    # amount of samples (H and var)
    max = 80
    c_value = [0.2, 0.4, 0.6, 0.8, 1]
    H_value = [2, 5, 7, 15, 25, 50]
    for i in range(len(c_value)):
        for j in range(len(H_value)):
            images_signal(t, triangular_signal, N, c_value[i], H_value[j], amplitude)
    
    c_index = 40
    H_index = 4 
    images_MSE(t, N, max, triangular_signal, c_index, H_index)
    
    
if __name__ == "__main__":
    main()

