from machine import Pin
import time
# value(0) -> on  ; value(1) -> off ??
# SWITCH = Pin(15, Pin.IN) 
LED1 = Pin(2, Pin.OUT)
#LED2 = Pin(5,Pin.OUT)
def led1():
    LED1.value(1)
    print("Praca rozpocznie się po wcisnieciu przycisku")
    i = 5
    while i > 0:
        # while SWITCH.value() == 0:
        #     pass  # Wait for the button press
        LED1.value(0)
        time.sleep(1)
        LED1.value(1)
        i -= 1
print("Test led 1")
led1()
