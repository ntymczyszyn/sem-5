def decimal_to_binary(decimal):
    binary = ""
    if decimal == 0:
        return "0"
    while decimal > 0:
        remainder = decimal % 2
        binary = str(remainder) + binary
        decimal = decimal // 2
    print("Wartosc w systemie dwojkowym: "+ binary)
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
    print("Wartosc w systemie szesnastkowym: "+ hexadecimal)
def driver():
    try:
        decimal_number = int(input("Podaj nieujemna liczbe dziesietną: "))
    except ValueError:
        print("ValueError - wprowadzona wartosc nie jest liczba naturalna, sprobuj ponownie.")
        return
    if decimal_number < 0:
        print("Wprowadzona liczba musi byc nieujemna!")
    else:
        try:
            system_choice = int(input("Wybierz system liczbowy (2 - dwojkowy, 16 - szesnastkowy): "))
        except ValueError:
            print("ValueError - wprowadzona wartosc nie jest liczba, sprobuj ponownie.")
            return
        if system_choice == 2:
            decimal_to_binary(decimal_number)
            choice = input("Czy podac liczbe w systemie szesnastkowym? (t/n): ")
        if choice == 'T' or choice == 't':
            decimal_to_hexadecimal(decimal_number)
        elif choice != 'N' or choice != 'n':
            print("Blad! Nieprawidlowy wybor.")
        elif system_choice == 16:
            decimal_to_hexadecimal(decimal_number)
            choice = input("Czy podac liczbe w systemie dwojkowym? (t/n): ")
        if choice == 'T' or choice == 't':
            decimal_to_binary(decimal_number)
        elif choice != 'N' or choice != 'n':
            print("Blad! Nieprawidlowy wybor.")
        else:
            print("Niepoprawny wybor systemu liczbowego.")
def main():
	on = True
	k = 't'
	driver()
	while(on):
		k = input("Kontynuowac? (t/n): ")  
		if k == 'N' or k == 'n':
			break
		elif k == 'T' or k == 't':
			driver()
		else: 
			print("Blad! Wprowadzono niepoprawna wartosc.")
			continue
main()