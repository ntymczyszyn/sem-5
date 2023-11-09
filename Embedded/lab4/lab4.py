from machine import Pin
import time
alphabet =[ {'A': [1,2]}, {'B': [2,1,1,1]}, {'C': [2,1,2,1]}, {'D': [2,1,1]},
            {'E': [1]}, {'F': [1,1,2,1]}, {'G': [2,2,1]}, {'H': [1,1,1,1]},
            {'I': [1,1]}, {'J': [1,2,2,2]}, {'K': [2,1,2]}, {'L': [1,2,1,1]},
            {'M': [2,2]}, {'N': [2,1]},{'O': [2,2,2]},{'P': [1,2,2,1]},
            {'Q': [2,2,1,2]}, {'R': [1,2,1]}, {'S': [1,1,1]}, {'T': [2]},
            {'U': [1,1,2]}, {'V': [1,1,1,2]}, {'W': [1,2,2]}, {'X': [2,1,1,2]},
            {'Y': [2,1,2,2]}, {'Z': [2,2,1,1]}]
def driver():
    led = Pin(2, Pin.OUT)
    led.on()
    word = input("Prosze podac slowo:  ")
    word = word.upper()
    parsed_word = ""
    for i in range(len(word)):
          if (word[i].isalpha()):
                parsed_word = parsed_word + word[i]   
    if (len(parsed_word) != len(word)):
          print("Podano znak spoza alfabetu!")
    else:
        for i in range(len(parsed_word)):
            morse_letter = alphabet[ord(parsed_word[i]) - ord('A')][parsed_word[i]]
            for j in range(len(morse_letter)):
                if (morse_letter[j] == 1):
                    # krótkie świecenie
                    led.off() # ??
                    time.sleep_ms(500)
                    led.on()
                    print("krotkie")
                elif (morse_letter[j] == 2):
                    # długie świecenie
                    led.off()
                    time.sleep_ms(1000)
                    led.on()
                    print("dlugie")
                time.sleep_ms(200)# przerwa bardzo krótka
            time.sleep_ms(100)# przerwa między literami
        # przerwa między słowami - naraziejedno slowo  
def main():
	k = 't'
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
