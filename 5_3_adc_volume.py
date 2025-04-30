import RPi.GPIO as GPIO
import time

leds = [2, 3, 4, 17, 27, 22, 10, 9]
leds_amount = len(leds)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
aux = [0] * leds_amount
comp = 14
troyka = 13
sleep_time = 0.001

GPIO.setmode(GPIO.BCM)

GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec_to_bin(num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]

def adc():
    adc_val = 128
    GPIO.output(dac, dec_to_bin(adc_val))
    time.sleep(sleep_time)

    adc_val += 64 + (-128) * GPIO.input(comp)
    GPIO.output(dac, dec_to_bin(adc_val))
    time.sleep(sleep_time)

    adc_val += 32 + (-64) * GPIO.input(comp)
    GPIO.output(dac, dec_to_bin(adc_val))
    time.sleep(sleep_time)

    adc_val += 16 + (-32) * GPIO.input(comp)
    GPIO.output(dac, dec_to_bin(adc_val))
    time.sleep(sleep_time)

    adc_val += 8 + (-16) * GPIO.input(comp)
    GPIO.output(dac, dec_to_bin(adc_val))
    time.sleep(sleep_time)

    adc_val += 4 + (-8) * GPIO.input(comp)
    GPIO.output(dac, dec_to_bin(adc_val))
    time.sleep(sleep_time)

    adc_val += 2 + (-4)*GPIO.input(comp)
    GPIO.output(dac, dec_to_bin(adc_val))
    time.sleep(sleep_time)

    adc_val += 1 + (-2) * GPIO.input(comp)
    GPIO.output(dac, dec_to_bin(adc_val))
    time.sleep(sleep_time)

    adc_val = adc_val - 1 * GPIO.input(comp)

    return adc_val

try:
    while(True):
        signal = adc()
        volume = round(signal/(32))

        for i in range(0, volume):
            aux[i] = 1

        GPIO.output(leds, aux)
        voltage = signal * 3.3 / 255

        aux = [0] * leds_amount

        print(f"Signal = {signal} voltage = {voltage:.4}")
        
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()