def decimal_to_binary(decimal):
    binary = ""
    if decimal == 0:
        return "0"
    while decimal > 0:
        remainder = decimal % 2
        binary = str(remainder) + binary
        decimal = decimal // 2
    return binary

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
    return hexadecimal

def sterowanie():
    try:
        decimal_number = int(input("Podaj liczbę dziesiętną: "))
        if decimal_number < 0:
            print("Wprowadzona liczba musi być nieujemna.")
            return

        system_choice = input("Wybierz system liczbowy (2 - dwójkowy, 16 - szesnastkowy): ")

        if system_choice == "2":
            binary_number = decimal_to_binary(decimal_number)
            print(f"Wartość w systemie dwójkowym: {binary_number}")
        elif system_choice == "16":
            hexadecimal_number = decimal_to_hexadecimal(decimal_number)
            print(f"Wartość w systemie szesnastkowym: {hexadecimal_number}")
        else:
            print("Niepoprawny wybór systemu liczbowego.")

    except ValueError:
        print("Wprowadzono niepoprawną liczbę dziesiętną.")

def main():
    on = True
    while(on):
        sterowanie()
        k = input("Kontynuowac? (t/n) : ") 
        if k == 'N' or k == 'n':
            on = False
