import RPi.GPIO as GPIO

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def dec_to_bin(num):
    bin_nums = [int(x) for x in bin(num)[2:]]
    zeros = [0 for i in range(8 - len(bin_nums))]
    zeros += bin_nums
    return zeros

try:
    while True:
        inp = input("Please enter a number:")
        
        if inp == "q":
            print("exiting")
            break

        try:
            num_int = int(inp)
        except Exception:
            try:
                numfl = float(inp)
                print("Enter from 0 to 255, not float")
            except Exception:
                print("Enter from 0 to 255, not symbol")                
            continue

        if int(inp) < 0:
            print("Should be positive")
            continue
        
        if int(inp) > 255:
            print("Should be less 256")
            continue
        
        GPIO.output(dac, dec_to_bin(int(inp)))
        volts = float(inp) / 256.0 * 3.3
        print(f"Excepted voltage is {volts:.6}")


finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup()