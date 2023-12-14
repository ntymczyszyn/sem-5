import network
import socket
from machine import Pin
import time
alphabet =[ {'A': [1,2]}, {'B': [2,1,1,1]}, {'C': [2,1,2,1]}, {'D': [2,1,1]},
            {'E': [1]}, {'F': [1,1,2,1]}, {'G': [2,2,1]}, {'H': [1,1,1,1]},
            {'I': [1,1]}, {'J': [1,2,2,2]}, {'K': [2,1,2]}, {'L': [1,2,1,1]},
            {'M': [2,2]}, {'N': [2,1]},{'O': [2,2,2]},{'P': [1,2,2,1]},
            {'Q': [2,2,1,2]}, {'R': [1,2,1]}, {'S': [1,1,1]}, {'T': [2]},
            {'U': [1,1,2]}, {'V': [1,1,1,2]}, {'W': [1,2,2]}, {'X': [2,1,1,2]},
            {'Y': [2,1,2,2]}, {'Z': [2,2,1,1]}]
led = Pin(2, Pin.OUT) 
def morse_code(parsed_word):
    for letter in parsed_word:
        for morse_signal in alphabet[ord(letter) - ord('A')][letter]:
            led.off() # zalaczenie diody
            if morse_signal == 1:
                time.sleep_ms(500)
            elif morse_signal == 2:
                time.sleep_ms(1000)
            led.on()
            time.sleep_ms(200)
        time.sleep_ms(100)  # Przerwa między literami
def handle_telnet_connection(client_socket):
    # tytuł
    client_socket.sendall(b"Word to Morse Code converter\n")
    try:
        while True:
            # wysyłamy informacje na terminal klienta
            client_socket.sendall("Prosze podac slowo:  ")
            # pobieramy dane ze zdalnego terminalu
            # 1024 bajty naraz, konwerujemy do string (kodowane utf-8), usuwamy białe znaki
            data = client_socket.recv(1024).decode('utf-8').strip()
            if not data:
                break
            data_upper = data.upper()
            parsed_word = ""
            for char in data_upper:
                if (char.isalpha()):
                    parsed_word = parsed_word + char   
            if (len(parsed_word) != len(data)):
                client_socket.sendall("Podano znak spoza alfabetu!")
            else:
                morse_code(parsed_word)
    #idk czy tu powinnimy jakas obsluge zakonczenia robic czy nie?
    except Exception as e:
        print("Blad:", e) # tego chyba damy rady wyslac klientowi ja dostalismy blad
    finally: # zawsze się wykona - nawet jeśli bedzie blad
        client_socket.close()
def telnet_server():
    # ESP8266 jako Access Point
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="ESP8266-AP", password="password123")
    # utworzenie socketu (z protokołami IPv4 i TCP - połączenie strumieniowe)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 23 - standardowy port Telnet
    # 0.0.0.0 - serwer będzie nasłuchiwał na wszystkich dostępnych interfejsach sieciowych
    # idk czy możemy jakiś konkretny interfejs ustawić
    server_socket.bind(('0.0.0.0', 23))
    # uruchamienie serwer w trybie nasłuchiwania na przychodzące połączenia. 
    # 1 - serwer akceptuje jedno połączenie w danym momencie
    server_socket.listen(1)
    while True:
        # oczekiwanie na połączenie
        client_socket, client_addr = server_socket.accept()
        print("Polaczenie z: ", client_addr) # wypisze to w interpreterze MicroPythona
        handle_telnet_connection(client_socket)
if __name__ == "__main__":
    telnet_server()
