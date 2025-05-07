import RPi.GPIO as GPIO
import time

#pins selection
leds = [2, 3, 4, 17, 27, 22, 10, 9]
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

#constants selection
sleep_time = 0.001 # time interval between adc measurements
adc_max_val = 255
vol_max_val = 3.3
cap_max_val = 1.88
task_max_val = 0.97 * adc_max_val * cap_max_val / vol_max_val
task_min_val = 0.02 * adc_max_val * cap_max_val / vol_max_val

#pins initializing
GPIO.setmode(GPIO.BCM)

GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(comp, GPIO.IN)

#return binary array of num
def dec_to_bin(num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]

#return value from 0 to 255 on comparator pin
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

# show binary num on pins from dac
def show_num_on_leds(num):
    bin_num = dec_to_bin(num)
    GPIO.output(dac, bin_num)
    return 0

voltage_vals = []
time_vals = []

try:
    exp_start = time.time()
    GPIO.output(troyka, GPIO.HIGH)

    troyka_signal = 0
    print(GPIO.HIGH)
    # time.sleep(100)
    while(troyka_signal < task_max_val):
        troyka_signal = adc()
        # print(troyka_signal, task_max_val)
        voltage_vals.append(troyka_signal)
        time_vals.append(time.time() - exp_start)

    GPIO.output(troyka, 0)
    while(troyka_signal > task_min_val):
        troyka_signal = adc()
        print(troyka_signal, task_min_val, time.time())
        voltage_vals.append(troyka_signal)
        time_vals.append(time.time() - exp_start)

    exp_end = time.time()
    print(f"Experiment lasted for {exp_end-exp_start}s")
        
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()