# from machine import Pin
import time
from numpy import char

# Do przycisków:
# przycisk_pin = Pin(0, Pin.IN, Pin.PULL_UP)  # Ustawienie pinu przycisku (dla przykładu użyto pinu numer 0)

# while True:
#     if przycisk_pin.value() == 0:
#         print("Przycisk został naciśnięty.")

# USTAWIENIE PINOW
joints_OFF =  [[1,5],[2,8]]
joint_ON = [[1,6],[2,7]]


def INFO():
    print("----- PRZEKAZNIK CZASOWY PCU-520 -----")
    print("--- SPOSOB DZIALANIA ---")
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

    if ( choice == 1 ):
        try:
            print("FUNCJE: \nA. Opoznione wylaczanie \nB. Opoznione zalaczanie \nC. Opoznione wylaczenie-cykliczne \nD. Opoznione zalaczenie-cykliczne")
            auto_choice = (input("Wybor: "))
        except ValueError:
            print("ValueError - wprowadzona wartosc jest nieprawidłowa")
            return 
        return auto_choice
    elif ( choice == 2 or choice == 3):
        return choice
    else:
        print("Blednie dane, sprobuj ponownie")
        return MENU() # Mozna tak?

def LED_PULS():
    for i in range(0,120):
        # zapal/zgas diode
        time.sleep(0.01)
        #zgas/ zapal diode
        time.sleep(0.01)

def A():
    try:
        t1 = float(input("Podaj t1 [3s - 20s]: ")) 
        t2 = float(input("Podaj t2 [3s - 20s]: "))
    except ValueError:
        print("ValueError - wprowadzona wartosc nie niepoprawna, sprobuj ponownie.")
        return
    if( t1 < 2 or t2 < 2):
        print("Za male wartosci")
    # zaczynamy od stykow na joint_OFF
    start = input("Praca rozpocznie się po wcisnieciu przycisku ...")
    if start == 'a':
        # ustawienie stykow na joint_ON
        time.sleep(t1-2)
        LED_PULS()
        # ustawienie styków na joint_OFF
        time.sleep(t2-2)
        LED_PULS
        # ustawienie stykow na joint_ON
        print("ok")
        return

def B():
    try:
        t1 = float(input("Podaj t1 [3s - 20s]: ")) 
        t2 = float(input("Podaj t2 [3s - 20s]: "))
    except ValueError:
        print("ValueError - wprowadzona wartosc nie niepoprawna, sprobuj ponownie.")
        return
    # zaczynamy od stykow na joint_OFF
    start = input("Praca rozpocznie się po wcisnieciu przycisku ...")
    if start == 'a':
        # styki na joint_OFF
        time.sleep(t1)
        # ustawienie styków na joint_ON
        time.sleep(t2)
        # ustawienie stykow na joint_OFF
        return

def C():
    try:
        t1 = float(input("Podaj t1 [3s - 20s]: ")) 
        t2 = float(input("Podaj t2 [3s - 20s]: "))
    except ValueError:
        print("ValueError - wprowadzona wartosc nie niepoprawna, sprobuj ponownie.")
        return
    # zaczynamy od stykow na joint_OFF
    start = input("Praca rozpocznie się po wcisnieciu przycisku ...")
    if start == 'a':
        i=0 # do zmiany na przycisk ??
        while(i < 10):
            # ustawienie stykow na joint_ON
            time.sleep(t1)
            # ustawienie styków na joint_OFF
            time.sleep(t2)
            # ustawienie stykow na joint_ON
            i += 1
        return

def D():
    try:
        t1 = float(input("Podaj t1 [3s - 20s]: ")) 
        t2 = float(input("Podaj t2 [3s - 20s]: "))
    except ValueError:
        print("ValueError - wprowadzona wartosc nie niepoprawna, sprobuj ponownie.")
        return
    # zaczynamy od stykow na joint_OFF
    start = input("Praca rozpocznie się po wcisnieciu przycisku ...")
    # ustawienie stykow na joint_ON
    if start == 'a':
        i=0 # do zmiany na przycisk ??
        while(i < 10):
            # styki sa na joint_OFF
            time.sleep(t1)
            # ustawienie stykow na joint_ON
            time.sleep(t2)
            # ustawienie styków na joint_OFF
            i += 1
        return

def MANUAL_BI():
    i = 0 # do zmiany na przycisk ??
    while(i < 10):
        i += 1
        if( True):
            print("zmiana stanu")

    return

def MANUAL_MONO():
    i = 0 # do zmiany na przycisk ??
    while(i < 10):
        i += 1
        if( True):
            print("zasilanie przez 1 s")
            time.sleep(1)
    return

def driver():
    choice = MENU()
    if choice == 'A' or choice == 'a':
        A()
    elif choice == 'B' or choice == 'b':
        B()
    elif choice == 'C' or choice == 'c':
        C()
    elif choice == 'D' or choice == 'd':
        D()
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