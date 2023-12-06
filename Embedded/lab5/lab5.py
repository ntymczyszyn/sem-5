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
    print("Styki pozostaja w pozycji 1-5, 2-8 (OFF) do czasu zalaczenia. Po podaniu napiecia zasilajacego przelaczone zostaja w pozycja 1-6, 2-7(ON).")
    print("\t ---- SPOSOB DZIALANIA TRYBU AUTO ----")
    print("A - OPOZNIONE WYLACZENIE \nDo czasu zalaczenia przekaznika styki pozostaja w pozycji 1-5, 2-8.\nPo podaniu napiecia zasilajacego styki zostaja przelaczone w pozycje 1-6, 2-7 na czas t1. \nPo odmierzeniu czasu t1 styki powracaja do pozycji 1-5, 2-8 na czas t2. \nPo czasie t2 styki przekaznika powracaja do pozycji 1-6, 2-7. \nPonowna realizacja trybu pracy przekaznika mozliwa jest po odlaczeniu napiecia zasilajacego i ponownym jego zalaczeniu.")
    print("B - OPOZNIONE ZALACZENIE \nPo podaniu napiecia zasilajacego styki pozostaja w pozycji 1-5, 2-8 przez czas t1. \nPo odmierzeniu czasu t1 nastepuje przelaczenie stykow w pozycje 1-6, 2-7 na czas t2. \nPo czasie t2 styki przekaznika powracaja do pozycji 1-5, 2-8. \nPonowna realizacja trybu pracy przekaznika mozliwa jest po odlaczeniu napiecia zasilajacego i ponownym jego zalaczeniu.")
    print("C - OPOZNIONE WYLACZENIE - CYKLICZNIE \nTryb pracy opoznionego wylaczania realizowany cyklicznie w ustawionych odstepach czasu pracy i przerwy.")
    print("D - OPOZNIONE ZALACZENIE - CYKLICZNIE \nTryb pracy opoznionego zalaczania realizowany cyklicznie w ustawionych odstepach czasu pracy i przerwy.") 
    return
def MENU():
    try:
        choice = int(input("TRYBY PRACY: \n1. AUTO \n2.MANUAL_BI \n3.MANUAL_MONO \nWybor: "))
    except ValueError:
        print("ValueError - wprowadzona wartosc nie jest liczba naturalna, sprobuj ponownie.")
        return
    if (choice == 1 or choice == 2 or choice == 3):
        return choice
    else:
        print("Blednie dane, sprobuj ponownie")
        return MENU() # Mozna tak? najwyraźniej --N
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
        print("ValueError - wprowadzona wartosc jest niepoprawna, sprobuj ponownie.")
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
        return # dodane
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
    return # tu w sumie return if przycisk pressed i we wszystkich AUTO
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
        LED1.value(not LED1.value()) # czy to napewno zdziała??
    #return usunełam bo i tak nie podtzebny
def MANUAL_MONO():
    while(True):
        while SWITCH.value() == 0:
            pass  # Wait for the button press
        LED1.value(0)
        time.sleep(1)
        LED1.value(1)
    # ti tak samo jak w _BI
def driver():
    choice = MENU()
    if choice == 1:
        AUTO()
    elif choice == 2:
        MANUAL_BI()
    elif choice == 3:
        MANUAL_MONO()
    # else: # to się chyba nigdy nie wykona??
    #     print("Nieprawidłowy wybór.")
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