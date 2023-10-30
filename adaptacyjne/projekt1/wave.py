import matplotlib.pyplot as plt
import numpy as np
import random
import os
from matplotlib import cm

# number of samples, max h, expected signal 
def calculate_all(N, max, triangular_signal):
    H = [i for i in range(2,max + 2)]
    c = np.linspace(0.2, 5.2, max) # numbers chosen arbitrarily
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
            estimated =[ local_sum[i]/(H[current_h]) if (i > H[current_h]) else triangular_signal[i]  for i in range(N)]
           
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

    estimated =[ local_sum[i]/(H) if (i > H) else triangular_signal_with_noise[i]  for i in range(N)]

    for i in range(H, N): # od H do N
        MSE += (triangular_signal_with_noise[i] - estimated[i])**2
    MSE = MSE/(N - H)
    return triangular_signal_with_noise, estimated, MSE

def main():
    # triangular function parameters 
    frequency = 0.01  # Frequency of the signal (cycles per second)
    period = 1 / frequency
    amplitude = 1.0  # Amplitude of the signal
    duration = 1000.0  # Duration of the signal (seconds)
    sampling_frequency = 0.7  # Sampling frequency (samples per second)
    # time vector
    t = np.linspace(0, duration, int(sampling_frequency * duration), endpoint=False) # <class 'numpy.ndarray'>
    N = len(t)
    # triangular_signal = amplitude * (2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1)
    triangular_signal = ((4 * amplitude) / period) * np.abs(((t - (period * 0.25))%period) - (period * 0.5)) - amplitude
    # amount of samples (H and var)
    max = 10
    # calculating MSE, H and var
    H, MSE, var, H_opt, MSE_opt = calculate_all(N, max, triangular_signal)
    t_w_n, est, MSE_ = estimate(triangular_signal, N, c=5, H=10)
    # creating plots
    # signal w/ and wo/ noise
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111) # TE NAZWY SĄ DO ZMIANY !
    # TRZEBABY JESZCZE POKAZAĆ TEN ESTYMOWANY SYGNAŁ(?)
    ax.plot(t, triangular_signal, c='r', label="Fala trójkątna") 
    # ax.plot(t, est, c='b', marker='o', label="Fala estymowana")
    ax.scatter(t, t_w_n, c='g', marker='o', label="Zaszumiona fala trójkątna")
    ax.set_title(f'Fala trójkątna')
    ax.legend(loc='upper right')
    ax.set_xlabel('Czas (s)')
    ax.set_ylabel('Amplituda')
    # ax.set_ylim(-amplitude - 0.5, amplitude + 0.5)
    fig_est = plt.figure(figsize=(10,8))
    ax_est = fig_est.add_subplot(111)
    ax_est.plot(t, triangular_signal, c='r', label="Fala trójkątna") 
    ax_est.plot(t, est, c='b', marker='o', label="Fala estymowana")
    # ax_est.scatter(t, t_w_n, c='g', marker='o', label="Zaszumiona fala trójkątna")
    ax_est.set_title(f'Fala trójkątna')
    ax_est.legend(loc='upper right')
    ax_est.set_xlabel('Czas (s)')
    ax_est.set_ylabel('Amplituda')

    # MSE(H) and MSE(var) plots
    fig_MSE, (ax_H, ax_var) = plt.subplots(1, 2, figsize=(12, 6))
    #  H
    c_value = 5
    ax_H.scatter(H, MSE[c_value , :], color='b', marker='o', s=10)
    ax_H.set_title(f'Zależność MSE(H) dla var ={(2 * (c_value**2)) / 3}')
    ax_H.set_xlabel('Horyzont pamięci')
    ax_H.set_ylabel('MSE(H)')
    # var
    H_value = 2
    ax_var.scatter(var, MSE[: , 0] , color='r', marker='o', s=10)
    ax_var.set_title(f'Zależność MSE(H) przy różnych wariacjach dla H = {H_value}')
    ax_var.set_xlabel('Wariancja')
    ax_var.set_ylabel('MSE')

    # Var(H opt) - CZY TO NIE POWINNO BYĆ NA ODWRÓT Hopt(var) ?? 
    fig_opt = plt.figure(figsize=(8, 6))
    ax_opt = fig_opt.add_subplot(111)
    ax_opt.scatter(var, H_opt,  c='r', s=10) # ZAMIENIŁAM TUTAJ KOLEJNOŚĆ!!
    ax_opt.set_title('H optymalne(wariancja)')
    ax_opt.set_ylabel('Optymalny horyzont pamięci')
    ax_opt.set_xlabel('Wariancja')

    # 3d plot - H, var, MSE(h) + h opt for all calculated var
    fig_3d = plt.figure(figsize=(8, 6))
    ax0 = fig_3d.add_subplot(111, projection='3d')
    X, Y = np.meshgrid(H, var)
    Z = MSE

    # optimal horizon plot
    ax0.scatter(H_opt, var, MSE_opt, c='black', marker='o', s=20, label="H opt(var)")

    # norm = plt.Normalize(Z.min(), Z.max())
    colors = cm.rainbow(Z)
    rcount, ccount, _ = colors.shape
    surf = ax0.plot_surface(X, Y, Z, rcount=rcount, ccount=ccount, facecolors=colors, shade=False)
    # surf.set_facecolor((0,0,0,0))
    # cbar = fig.colorbar(surf, shrink=0.5, aspect=5)

    ax0.set_xlabel('Horyzont pamięci')
    ax0.set_ylabel('Wariancja')
    ax0.set_zlabel('MSE(H)')
    ax0.set_title('MSE(H) dla róznych wariancji')
    ax0.legend(loc='center left', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(__file__), "images", "Wykres_szumu.png"), dpi=500)
    fig_est.savefig(os.path.join(os.path.dirname(__file__), "images", "Wykres_estymowany.png"), dpi=500)
    fig_3d.savefig(os.path.join(os.path.dirname(__file__), "images", "Wykres_3d.png"), dpi=500)
    fig_opt.savefig(os.path.join(os.path.dirname(__file__), "images", "Wykres_opt.png"), dpi=500)
    fig_MSE.savefig(os.path.join(os.path.dirname(__file__), "images", "Wykres_MSE.png"), dpi=500)

    # plt.show()

if __name__ == "__main__":
    main()
"""
plt.figure(1)
plt.scatter(H, MSE_H, c='b', marker='o')
plt.scatter(min_H, min_MSE, c='r', marker='o', label=f'Min MSE (H={min_H}, MSE={min_MSE})')
plt.title(f'MSE(H) for c = {c}')
plt.xlabel('H')
plt.ylabel('MSE')
plt.show()

plt.figure()
plt.plot(var, MSE_c,c='b', marker='o')
# plt.scatter(min_var, min_MSE_c, c='r', marker='o', label=f'Min MSE (var={min_var}, MSE={min_MSE_c})')
# plt.title(f'MSE(var) for c = {c}')
plt.xlabel('var')
plt.ylabel('MSE')
plt.show()
"""
# print(f"MSE: {min_MSE_H}  H: {min_H}  var: {min_var}")
"""
plt.figure()
plt.plot(t, triangular_signal, c='r') 
plt.scatter(t, triangular_signal_with_noise, c='b', marker='o')
plt.title('Triangular Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.ylim(-amplitude - 0.5, amplitude + 0.5) 
plt.show()


# plt.figure(figsize=(12, 8))  
# plt.plot(t, triangular_signal, c='r')
# plt.plot(t, estimated_Q, c='b', marker='o')
# plt.scatter(t, triangular_signal_with_noise, c='g')
# plt.show()
# # -------------------------------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(14, 5))
axs[0].plot(t, triangular_signal, c='r')
axs[0].plot(t, estimated_Q, c='b', marker='o')
axs[0].scatter(t, triangular_signal_with_noise, c='g')
axs[0].set_title('Triangular Wave with the estimate')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('Amplitude')

# axs[1].plot(t, estimated_Q, c='b')
# axs[1].plot(t, triangular_signal_with_noise, c='g')
# axs[1].set_title('Noisy Triangular Wave and the estimate')
axs[1].scatter(H, MSE, c='b', marker='o')
axs[1].set_title(f'MSE(H) for c = {c}')
axs[1].set_xlabel('H')
axs[1].set_ylabel('MSE')
# axs[1].set_xlabel('Time')
# axs[1].set_ylabel('Amplitude')
plt.tight_layout()  
plt.show()
"""
