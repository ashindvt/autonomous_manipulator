import sys
import tty
import termios
from gpiozero import PWMOutputDevice
from time import sleep

# Define the 4 PWM pins for MDD3A
# Left Motor
m1a = PWMOutputDevice(23) 
m1b = PWMOutputDevice(18)
# Right Motor
m2a = PWMOutputDevice(24)
m2b = PWMOutputDevice(19)

def stop():
    m1a.value = 0; m1b.value = 0
    m2a.value = 0; m2b.value = 0

def forward():
    m1a.value = 0; m1b.value = 0.5 # M1 Forward
    m2a.value = 0; m2b.value = 0.5 # M2 Forward

def backward():
    m1a.value = 0.5; m1b.value = 0 # M1 Reverse
    m2a.value = 0.5; m2b.value = 0 # M2 Reverse

def left():
    m1a.value = 0; m1b.value = 0.5 # M1 Reverse
    m2a.value = 0.5; m2b.value = 0 # M2 Forward

def right():
    m1a.value = 0.5; m1b.value = 0 # M1 Forward
    m2a.value = 0; m2b.value = 0.5 # M2 Reverse

print("Use W-A-S-D to move, Space to stop, Q to quit")

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

try:
    while True:
        char = getch()
        if char == 'w': forward()
        elif char == 's': backward()
        elif char == 'a': left()
        elif char == 'd': right()
        elif char == ' ': stop()
        elif char == 'q': break
finally:
    stop()