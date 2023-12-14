# from machine import Pin
import time
alphabet =[ {'A': [1,2]}, {'B': [2,1,1,1]}, {'C': [2,1,2,1]}, {'D': [2,1,1]},
            {'E': [1]}, {'F': [1,1,2,1]}, {'G': [2,2,1]}, {'H': [1,1,1,1]},
            {'I': [1,1]}, {'J': [1,2,2,2]}, {'K': [2,1,2]}, {'L': [1,2,1,1]},
            {'M': [2,2]}, {'N': [2,1]},{'O': [2,2,2]},{'P': [1,2,2,1]},
            {'Q': [2,2,1,2]}, {'R': [1,2,1]}, {'S': [1,1,1]}, {'T': [2]},
            {'U': [1,1,2]}, {'V': [1,1,1,2]}, {'W': [1,2,2]}, {'X': [2,1,1,2]},
            {'Y': [2,1,2,2]}, {'Z': [2,2,1,1]}]
# led = Pin(2, Pin.OUT)
def morse_code(parsed_word):
    for letter in parsed_word:
        for morse_signal in alphabet[ord(letter) - ord('A')][letter]:
            if (morse_signal == 1):
                # krótkie świecenie
                print("short")
                # led.off() # ??
                #time.sleep_ms(500)
                # led.on()
            elif (morse_signal == 2):
                print("long")
                # długie świecenie
                # led.off()
                #time.sleep_ms(1000)
                # led.on()
            #time.sleep_ms(200) # przerwa bardzo krótka
        #time.sleep_ms(100) # przerwa między literami
    # przerwa między słowami - na razie jedno slowo  

def input_handler():
    word = input("Prosze podac slowo:  ").upper()
    parsed_word = ""
    for char in word:
          if (char.isalpha()):
                parsed_word = parsed_word + char   
    if (len(parsed_word) != len(word)):
          print("Podano znak spoza alfabetu!")
    else:
        morse_code(parsed_word)
      
def main():
	k = 't'
	input_handler()
	while(True):
		k = input("Kontynuowac? (t/n): ")  
		if k == 'N' or k == 'n':
			break
		elif k == 'T' or k == 't':
			input_handler()
		else: 
			print("Blad! Wprowadzono niepoprawna wartosc.")
			continue  
main()
