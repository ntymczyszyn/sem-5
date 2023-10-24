def decimal_to_binary(decimal):
    binary = ""
    if decimal == 0:
        return "0"
    while decimal > 0:
        remainder = decimal % 2
        binary = str(remainder) + binary
        decimal = decimal // 2
    print(f"Wartosc w systemie dwojkowym: {binary}")

def decimal_to_hexadecimal(decimal):
    hexadecimal = ""
    if decimal == 0:
        return "0"
    while decimal > 0:
        remainder = decimal % 16
        if remainder < 10:
            hexadecimal = str(remainder) + hexadecimal
        else:
            hexadecimal = chr(ord('A') + remainder - 10) + hexadecimal
        decimal = decimal // 16
    print(f"Wartosc w systemie szesnastkowym: {hexadecimal}")

def driver():
    try:
        decimal_number = int(input("Podaj nieujemna liczbe dziesietną: "))
        if decimal_number < 0:
            print("Wprowadzona liczba musi byc nieujemna!")
        else:
            system_choice = input("Wybierz system liczbowy (2 - dwojkowy, 16 - szesnastkowy): ")

            if system_choice == "2":
                decimal_to_binary(decimal_number)
                choice = input("Czy podac liczbe w systemie szesnastkowym? (t/n): ")
                if choice == 'T' or choice == 't':
                    decimal_to_hexadecimal(decimal_number)
            elif system_choice == "16":
                decimal_to_hexadecimal(decimal_number)
                choice = input("Czy podac liczbe w systemie dwojkowym? (t/n): ")
                if choice == 'T' or choice == 't':
                    decimal_to_binary(decimal_number)
            else:
                print("Niepoprawny wybor systemu liczbowego.")

    except ValueError:
        print("ValueError - sprobuj ponownie.")

def main():
    on = True
    while(on):
        driver()
        k = input("Kontynuowac? (t/n) : ") 
        if k == 'N' or k == 'n':
            on = False
        # elif  k != 'T' or k != 't':
        #     print("Blad - sprobuj ponownie.")

main()
