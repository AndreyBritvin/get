import RPi.GPIO as GPIO

dac = [8, 11, 7, 1, 0, 5, 12, 6]

# pwm_pin = 27 # led
pwm_pin = 24 # RC

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.OUT)

pwm = GPIO.PWM(pwm_pin, 1000)
pwm.start(0)

try:
    while True:
        duty_cycle = float(input("Enter duty cycle from 0.0 to 100.0: "))
        pwm.ChangeDutyCycle(duty_cycle)
        volts = duty_cycle / 100 * 3.3
        print(f"Expected voltage: {volts:.4}")

finally:
    pwm.stop()
    GPIO.output(pwm_pin, GPIO.LOW)
    GPIO.cleanup()