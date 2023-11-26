import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import sawtooth

# Parametry funkcji prostokątnej
# od 1.5 do 2.5
amplituda_min = 1
amplituda_max = 1.2
czestotliwosc = 0.005  # Dla przykładu, możesz dostosować według potrzeb
czas_trwania = 1000
ilosc_probek = 500

# Generowanie czasu i wartości funkcji prostokątnej
czas = np.linspace(0, czas_trwania, ilosc_probek)
# funkcja_prostokatna = (amplituda_min + (amplituda_max - amplituda_min) / 2 * np.sign(np.sin(2 * np.pi * czestotliwosc * czas)))
# Parametry funkcji trójkątnej
amplituda = 0.1
czestotliwosc = 0.005
period = 1/czestotliwosc
czas_trwania = 1000
ilosc_probek = 500

# Generowanie czasu i wartości funkcji trójkątnej
czas = np.linspace(0, czas_trwania, ilosc_probek, endpoint=False)
# fala_trojkatna = amplituda * sawtooth(2 * np.pi * czestotliwosc * czas, 0.5) + 1
fala_trojkatna = ((4 * amplituda) / period) * np.abs(((czas - (period * 0.25))%period) - (period * 0.5)) - amplituda + 1

# Rysowanie funkcji prostokątnej
# plt.plot(czas, funkcja_prostokatna)
plt.plot(czas, fala_trojkatna )
# plt.title('Funkcja Prostokątna')
plt.xlabel('Czas')
plt.ylabel('Amplituda')
plt.grid(True)
plt.savefig('wykres.png')  
plt.show()