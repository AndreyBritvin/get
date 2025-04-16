import RPi.GPIO as GPIO
from time import sleep

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def dec_to_bin(num):
    bin_nums = [int(x) for x in bin(num)[2:]]
    zeros = [0 for i in range(8 - len(bin_nums))]
    zeros += bin_nums
    return zeros

try:
    period = float(input("Enter period:"))
    period /= 256 + 256

    while True:
        for i in range(0, 256):             # starts from 0 to 255
            GPIO.output(dac, dec_to_bin(i))
            sleep(period)
        
        for i in range(254, 0, -1):         # starts from 254 (skip 255 from prev) to 1 (skip 0 to next)
            GPIO.output(dac, dec_to_bin(i))
            sleep(period)

except Exception:
    print("Wrong input. Should be float")

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup()