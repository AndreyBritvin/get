import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec_to_bin(num):
    bin_nums = [int(x) for x in bin(num)[2:]]
    zeros = [0 for i in range(8 - len(bin_nums))]
    zeros += bin_nums
    return zeros

def adc():
    for i in range(0, 256):
        signal = dec_to_bin(i)
        GPIO.output(dac, signal)

        comp_signal = GPIO.input(comp)
        time.sleep(0.01)

        if comp_signal == GPIO.HIGH:
            return i

    return 0

try:
    while(True):
        signal = adc()
        voltage = signal * 3.3 / 255
        print(f"Signal = {signal} voltage = {voltage:.4}")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()