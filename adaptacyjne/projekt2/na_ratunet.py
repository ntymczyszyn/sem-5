    # Tworzenie danych przed pętlą 
    # Dla [0]
    u_k = np.zeros(N)
    u_k[0] = (v_wanted[0])
    Phi = np.array([[u_k[0]],
                    [0],
                    [0]])
    V_true[0] = b_true[0]*u_k[0]
    y_true[0] = V_true[0]  + noise[0]
    P_k = 1/Lambda * (P_k - (np.dot(np.dot(np.dot(P_k,Phi),Phi.T),P_k))/ (Lambda + np.dot(np.dot(Phi.T, P_k),Phi)))

    B_estimated = [ [0],
                    [0],
                    [0]]
    b_estimated[:,0] = (B_estimated + (y_true[0] - np.dot(Phi.T, B_estimated)) * np.dot(P_k,Phi)).reshape((3,)) 
    # DLa [1]
    u_k[1] = (v_wanted[1])/b_estimated[0, 0]
    Phi = np.array([[u_k[1]],
                    [u_k[0]],
                    [0]])
    V_true[1] = b_true[0]*u_k[1] + b_true[1]*u_k[0] 
    y_true[1] =  V_true[1] + noise[1]
    P_k = 1/Lambda * (P_k - (np.dot(np.dot(np.dot(P_k,Phi),Phi.T),P_k))/ (Lambda + np.dot(np.dot(Phi.T, P_k),Phi)))
   
    B_estimated = [ [b_estimated[0, 0]],
                    [b_estimated[1, 0]],
                    [b_estimated[2, 0]]]
    b_estimated[:,1] = (B_estimated + (y_true[1] - np.dot(Phi.T, B_estimated)) * np.dot(P_k,Phi)).reshape((3,)) 
    for k in range(2, N):
        u_k[k] = ((np.sin(2*np.pi/3 * k) + 1.5) -  (b_estimated[1, k-1]* u_k[k-1] + b_estimated[2, k-1]*u_k[k-2]))/b_estimated[0, k-1]
        Phi = np.array([[u_k[k]],
                        [u_k[k-1]],
                        [u_k[k-2]]])
        # Wyliczamy nowe wyjście na podstawie oczekiwanego wejścia?? z b_true
        V_true[k] =  (b_true[0]*u_k[k] + b_true[1]*u_k[k-1] + b_true[2]*u_k[k-2])
        y_true[k] = V_true[k] + noise[k]
        # Calculate P_k - macierz kowariancji P_k to P(k-1) a new_P_k to P(k)
        P_k = 1/Lambda * (P_k - (np.dot(np.dot(np.dot(P_k,Phi),Phi.T),P_k))/ (Lambda + np.dot(np.dot(Phi.T, P_k),Phi)))
        
        # Calculate b_estimated 
        B_estimated = [[b_estimated[0, k-1]],
                       [b_estimated[1, k-1]],
                       [b_estimated[2, k-1]]]
        b_estimated[:,k] = (B_estimated + (y_true[k] - np.dot(Phi.T, B_estimated)) * np.dot(P_k,Phi)).reshape((3,)) 
            
        V_estimated[k] =  (b_estimated[0, k]*u_k[k] + b_estimated[1, k]*u_k[k-1] + b_estimated[2, k]*u_k[k-2])
        y_estimated[k] = V_estimated[k] + noise[k]
    print(f"B = {b_estimated[:,49]}")    
