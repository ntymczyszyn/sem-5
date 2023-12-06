from machine import Pin
import time
# value(0) -> on  ; value(1) -> off ??
SWITCH = Pin(15, Pin.IN) 
LED1 = Pin(4, Pin.OUT)
LED2 = Pin(5,Pin.OUT) 
# LED1 = Pin('Y12',Pin.OUT)
# LED2 = Pin('Y11',Pin.OUT)
# SWITCH = Pin('Y13',Pin.IN)
def INFO():
    print("\t----- PRZEKAZNIK CZASOWY PCU-520 -----")
    print("\t ---- SPOSOB DZIALANIA AUTO ----")
    print("A - OPOZNIONE WYLACZENIE \n  Po przycisnieciu przycisku Ledy zapalaja sie. Nastepnie po czasie t1 zostaja znaszone na czas t2 po czym zostaja ponownie zapalone.")
    print("B - OPOZNIONE ZALACZENIE \n  Po przycisnieciu przycisku Ledy gasza sie. Po odmierzeniu czasu t1 nastepuje wlaczenie ledow na czas t2. Po tym czasie zostaja one wylaczone")
    print("C - OPOZNIONE WYLACZENIE - CYKLICZNIE \n Cyklicznie realizowany tryb pracy i przerwy w podanych czasach t1 i t2, rozpoczynajacy sie od wlaczenia ledu")
    print("D - OPOZNIONE ZALACZENIE - CYKLICZNIE \n Cyklicznie realizowany tryb pracy i przerwy w podanych czasach t1 i t2, rozpoczynajacy sie od wylaczenia ledu") 
    print("Przed zmiana stanu ledu przez 2 sekundy nastepuje szybkie zapalanie oraz gaszenie ledu 2.")
    return
def MENU():
    try:
        choice = int(input("TRYBY PRACY: \n1. AUTO \n2.MANUAL_BI \n3.MANUAL_MONO \nWybor: "))
    except ValueError:
        print("ValueError - wprowadzona wartosc nie jest liczba naturalna, sprobuj ponownie.")
        return
    if ( choice == 1 or choice == 2 or choice == 3):
        return choice
    else:
        print("Blednie dane, sprobuj ponownie")
        return MENU() # Mozna tak?
def AUTO():
    try:
        print("FUNCJE: \nA. Opoznione wylaczanie \nB. Opoznione zalaczanie \nC. Opoznione wylaczenie-cykliczne \nD. Opoznione zalaczenie-cykliczne")
        choice = str(input("Wybor: "))
    except ValueError:
        print("ValueError - wprowadzona wartosc jest nieprawidłowa")
        return 
    try:
        t1 = float(input("Podaj t1 [3s - 12s]: ")) 
        t2 = float(input("Podaj t2 [3s - 12s]: "))
    except ValueError:
        print("ValueError - wprowadzona wartosc nie niepoprawna, sprobuj ponownie.")
        return
    if (t1 > 2 or t2 > 2):
        if choice == 'A' or choice == 'a':
            A(t1, t2)
        elif choice == 'B' or choice == 'b':
            B(t1, t2)
        elif choice == 'C' or choice == 'c':
            C(t1, t2)
        elif choice == 'D' or choice == 'd':
            D(t1, t2)
    else:
        print("Za male wartosci")
def LED_PULS():
    for i in range(10):
        # zapal/zgas diode1
        LED2.value(not LED2.value())
        # time.sleep_ms(100)
        time.sleep(0.1)
        #zgas/ zapal diode
        LED2.value(not LED2.value())
        time.sleep(0.1)
def A(t1, t2):        
    print("Praca rozpocznie się po wcisnieciu przycisku")
    while SWITCH.value() == 0:
        pass  # Wait for the button press
    # wyłącz LED1
    LED1.value(0)
    time.sleep(t1-2)
    LED_PULS()
    # włącz LED1
    LED1.value(1)
    time.sleep(t2-2)
    LED_PULS
    # wyłącz Led
    LED1.value(0)
    return
def B(t1, t2):
    print("Praca rozpocznie się po wcisnieciu przycisku")
    while SWITCH.value() == 0:
        pass  # Wait for the button press
    # styki na joint_OFF
    LED1.value(1)
    time.sleep(t1-2)
    LED_PULS()
    # ustawienie styków na joint_ON
    LED1.value(0)
    time.sleep(t2-2)
    LED_PULS()
    # ustawienie stykow na joint_OFF
    LED1.value(1)
    return
def C(t1, t2):
    print("Praca rozpocznie się po wcisnieciu przycisku")
    while SWITCH.value() == 0:
        pass  # Wait for the button press
    i=0 # do zmiany na przycisk ??
    LED1.value(0) # zaczynamy na on
    while(i < 5):
        # zmiana stanu LED1
        LED1.value(not LED1.value())
        time.sleep(t1-2)
        LED_PULS()
        i += 1
    return
def D(t1, t2):
    print("Praca rozpocznie się po wcisnieciu przycisku")
    while SWITCH.value() == 0:
        pass  # Wait for the button press
    i=0 # do zmiany na przycisk ??
    LED1.value(1) # zaczynammy na off
    while(i < 5):
        # szmiana stanu LED1
        LED1.value(not LED1.value())
        time.sleep(t1-2)
        LED_PULS()
        i += 1
    return
def MANUAL_BI():
    while(True):
        while SWITCH.value() == 0:
            pass  # Wait for the button press
        LED1.value(not LED1.value())
    return
def MANUAL_MONO():
    while(True):
        while SWITCH.value() == 0:
            pass  # Wait for the button press
        LED1.value(0)
        time.sleep(1)
        LED1.value(1)
    return
def driver():
    choice = MENU()
    if choice == 1:
        AUTO()
    elif choice == 2:
        MANUAL_BI()
    elif choice == 3:
        MANUAL_MONO()
    else:
        print("Nieprawidłowy wybór.")
def main():
    INFO()
    driver()
    while(True):
        k = input("Kontynuowac? (t/n): ")  
        if k == 'N' or k == 'n':
            break
        elif k == 'T' or k == 't':
            driver()
        else: 
            print("Blad! Wprowadzono niepoprawna wartosc.")
            continue  
main()