from machine import Pin
import time
# Do przycisków: ???
# przycisk_pin = Pin(0, Pin.IN, Pin.PULL_UP)  # Ustawienie pinu przycisku (dla przykładu użyto pinu numer 0)
# Funkcja obsługująca naciśnięcie przycisku
# def obsluz_przycisk(pin):
#     print("Przycisk został naciśnięty!")
# # Przypisz funkcję obsługującą do przerwania na zmianę stanu pinu (naciśnięcie przycisku)
# przycisk_pin.irq(trigger=Pin.IRQ_FALLING, handler=obsluz_przycisk)
# USTAWIENIE PINOW
joints_OFF =  [[1,5],[2,8]]
joint_ON = [[1,6],[2,7]]
LED = Pin(2, Pin.OUT) # LED = Pin('Y12',Pin.OUT)
# LED_2 = Pin(0, Pin.OUT) 
# joint_off1 = [Pin(1, Pin.OUT),Pin(5, Pn.OUT)] ??
# joint_off2 = [Pin(2, Pin.OUT),Pin(8, Pin.OUT)]
# joint_on1 =  [Pin(1, Pin.OUT),Pin(6, Pin.OUT)]
# joint_on2 = [Pin(2, Pin.OUT),Pin(7, Pin.OUT)]
def INFO():
    print("\t----- PRZEKAZNIK CZASOWY PCU-520 -----")
    print("\t ---- SPOSOB DZIALANIA AUTO ----")
    print("Styki pozostaja w pozycji 1-5, 2-8 (OFF) do czasu zalaczenia. Po podaniu napiecia zasilajacego przelaczone zostaja w pozycja 1-6, 2-7(ON).")
    print("A - OPOZNIONE WYLACZENIE \nDo czasu zalaczenia przekaznika styki pozostaja w pozycji 1-5, 2-8.\nPo podaniu napiecia zasilajacego styki zostaja przelaczone w pozycje 1-6, 2-7 na czas t1. \nPo odmierzeniu czasu t1 styki powracaja do pozycji 1-5, 2-8 na czas t2. \nPo czasie t2 styki przekaznika powracaja do pozycji 1-5, 2-8 na czas t2. Po czasie t2 styki przekaznika powracaja do pozycji 1-6, 2-7. \nPonowna realizacja trybu pracy przekaznika mozliwa jest po odlaczeniu napiecia zasilajacego i ponownym jego zalaczeniu.")
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
        LED.value(not LED.value())
        # time.sleep_ms(100)
        time.sleep(0.1)
        #zgas/ zapal diode
        LED.value(not LED.value())
        time.sleep(0.1)
def A(t1, t2):        
    # zaczynamy od stykow na joint_OFF
    start = input("Praca rozpocznie się po wcisnieciu przycisku ...")
    if start == 'a':
        # ustawienie stykow na joint_ON
        LED.off()
        print("ON")
        time.sleep(t1-2)
        LED_PULS()
        # ustawienie styków na joint_OFF
        LED.on()
        print("OFF")
        time.sleep(t2-2)
        LED_PULS
        # ustawienie stykow na joint_ON
        LED.off()
        print("ON")
        return
def B(t1, t2):
    # zaczynamy od stykow na joint_OFF
    start = input("Praca rozpocznie się po wcisnieciu przycisku ...")
    if start == 'a':
        # styki na joint_OFF
        LED.on()
        print("OFF")
        time.sleep(t1-2)
        LED_PULS()
        # ustawienie styków na joint_ON
        LED.off()
        print("ON")
        time.sleep(t2-2)
        LED_PULS()
        # ustawienie stykow na joint_OFF
        LED.on()
        print("ON")
        return
def C(t1, t2):
    # zaczynamy od stykow na joint_OFF
    start = input("Praca rozpocznie się po wcisnieciu przycisku ...")
    if start == 'a':
        i=0 # do zmiany na przycisk ??
        while(i < 10):
            # ustawienie stykow na joint_ON
            LED.off()
            print("ON")
            time.sleep(t1-2)
            LED_PULS()
            # ustawienie styków na joint_OFF
            LED.on()
            print("OFF")
            time.sleep(t2-2)
            LED_PULS()
            i += 1
        return
def D(t1, t2):
    # zaczynamy od stykow na joint_OFF
    start = input("Praca rozpocznie się po wcisnieciu przycisku ...")
    # ustawienie stykow na joint_ON
    if start == 'a':
        i=0 # do zmiany na przycisk ??
        while(i < 10):
            # styki sa na joint_OFF
            LED.on()
            print("OFF")
            time.sleep(t1-2)
            LED_PULS()
            # ustawienie stykow na joint_ON
            LED.off()
            print("ON")
            time.sleep(t2-2)
            LED_PULS()
            i += 1
        return
def MANUAL_BI():
    i = 0 # do zmiany na przycisk ??
    while(i < 10):
        i += 1
        if( True):
            # LED.value(not led.value())
            print("zmiana stanu")
    return
def MANUAL_MONO():
    i = 0 # do zmiany na przycisk ??
    while(i < 10):
        i += 1
        if( True):
            # LED.off
            print("ON przez 1s")
            time.sleep(1)
            print("ON")
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