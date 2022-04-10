import RPi.GPIO as gpio
import time

pwmPin = 13
pwmPin2 = 12

def init() :
    global pwm
    global pwm2
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)
    gpio.setup(25, gpio.OUT)
    gpio.setup(5, gpio.OUT)
    gpio.setup(pwmPin2, gpio.OUT)
    gpio.setup(pwmPin, gpio.OUT)
    gpio.output(pwmPin, gpio.LOW)
    gpio.output(pwmPin2, gpio.LOW)
    pwm = gpio.PWM(pwmPin, 1000) # Set Frequency to 1 KHz
    pwm.start(0) # Set the starting Duty Cycle
    pwm2 = gpio.PWM(pwmPin2, 1000) # Set Frequency to 1 KHz
    pwm2.start(0) # Set the starting Duty Cycle

def destroy() :
    gpio.setmode(gpio.BCM)
    pwm.stop()
    gpio.output(pwmPin, gpio.LOW)
    pwm2.stop()
    gpio.output(pwmPin2, gpio.LOW)
    gpio.cleanup

def right(tf) :
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    dc = 50
    pwm.ChangeDutyCycle(dc)
    time.sleep(tf)
    destroy()

def left(tf) :
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    dc = 50
    pwm2.ChangeDutyCycle(dc)
    time.sleep(tf)
    destroy()

def forward(tf) :
    init()
    gpio.output(25, True)
    gpio.output(5, False)
    dc = 50
    pwm2.ChangeDutyCycle(dc)
    time.sleep(tf)
    destroy()

    print("fordward")
    right(5)
    print("backward")
    left(5)
    print("fordward")
    forward(5)
    destroy()

