import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

#pins selection
leds = [2, 3, 4, 17, 27, 22, 10, 9]
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

#constants selection
sleep_time = 0.001 # time interval between adc measurements
adc_max_val = 255
vol_max_val = 3.3
cap_max_val = 2.66
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
    val = 128
    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.0015)
    if GPIO.input(comp):
        val -= 64
    else:
        val += 64

    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.0015)
    if GPIO.input(comp):
        val -= 32
    else: 
        val += 32
    

    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.0015)
    if GPIO.input(comp):
        val -= 16
    else: 
        val += 16


    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.0015)
    if GPIO.input(comp):
        val -= 8
    else: 
        val += 8


    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.0015)
    if GPIO.input(comp):
        val -= 4
    else: 
        val += 4

    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.0015)
    if GPIO.input(comp):
        val -= 2
    else:
        val += 2

    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.0015)
    if GPIO.input(comp):
        val -= 1
    else: 
        val += 1


    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.0015)
    if GPIO.input(comp):
        val -= 1
    
    return val


# show binary num on pins from dac
def show_num_on_leds(num):
    bin_num = dec_to_bin(num)
    GPIO.output(dac, bin_num)

voltage_vals = []
time_vals = []

try:
    exp_start = time.time()
    GPIO.output(troyka, GPIO.HIGH)

    troyka_signal = 0
    # print(GPIO.HIGH)
    # time.sleep(100)
    while(troyka_signal < 245):
        troyka_signal = adc()
        # print(troyka_signal, task_max_val)
        voltage_vals.append(troyka_signal)
        time_vals.append(time.time()-exp_start)

    GPIO.output(troyka, 0)
    while(troyka_signal > 192):
        troyka_signal = adc()
        # print(troyka_signal, task_min_val, time.time())
        voltage_vals.append(troyka_signal)
        time_vals.append(time.time()-exp_start)

    exp_end = time.time()
    exp_duration = exp_end - exp_start        
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()


with open("settings.txt", "w") as settings:
    settings.write(str(len(voltage_vals) / exp_duration))
    settings.write("\n")
    settings.write(str(cap_max_val / 256))

voltage_data_text = "\n".join([str(i) for i in voltage_vals])

with open("data.txt", "w") as data_file:
    data_file.write(voltage_data_text)

print("/-----------------------------------------------------------------\\")
print("| Results")
print("| Duration of experiment:", exp_duration, "s")
print("| Period:", exp_duration / len(voltage_vals), "s")
print("| Frequency:", len(voltage_vals) / exp_duration, "Hz")
print("| Quantization shift:", cap_max_val / 256, "V")
print("\-----------------------------------------------------------------/")

plt.plot(time_vals, voltage_vals)
plt.show()