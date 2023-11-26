import numpy as np
import matplotlib.pyplot as plt

# Parametry funkcji prostokątnej
# od 1.5 do 2.5
amplituda_min = 1
amplituda_max = 1.2
czestotliwosc = 0.005  # Dla przykładu, możesz dostosować według potrzeb
czas_trwania = 1000
ilosc_probek = 500

# Generowanie czasu i wartości funkcji prostokątnej
czas = np.linspace(0, czas_trwania, ilosc_probek)
funkcja_prostokatna = (amplituda_min + (amplituda_max - amplituda_min) / 2 * np.sign(np.sin(2 * np.pi * czestotliwosc * czas)))

# Rysowanie funkcji prostokątnej
plt.plot(czas, funkcja_prostokatna)
plt.title('Funkcja Prostokątna')
plt.xlabel('Czas')
plt.ylabel('Amplituda')
plt.grid(True)
plt.savefig('wykres.png')  
plt.show()