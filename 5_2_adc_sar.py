import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13
sleep_time = 0.001

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec_to_bin(num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]


def adc():
    adc_start = time.time()

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

    print(f"adc time = {time.time()-adc_start:.6} adc_progr = {time.time()-adc_start-sleep_time * 8:.6}")
    return adc_val

try:
    while(True):
        signal = adc()
        voltage = signal * 3.3 / 255
        print(f"Signal = {signal} voltage = {voltage:.4}")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()