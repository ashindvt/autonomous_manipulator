
import curses
from gpiozero import PWMOutputDevice, DigitalOutputDevice

# Setup Motor 1 (Right)
pwm1 = PWMOutputDevice(18)
dir1 = DigitalOutputDevice(23)
# Setup Motor 2 (Left)
pwm2 = PWMOutputDevice(19)
dir2 = DigitalOutputDevice(24)

speed = 1.0 # Set a safe testing speed (50%)

def main(stdscr):
    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.addstr("Use WASD to move, SPACE to stop, Q to quit")
    
    while True:
        key = stdscr.getch()
        
        if key == ord('w'):
            dir1.off(); dir2.off()
            pwm1.value = pwm2.value = speed
        elif key == ord('s'):
            dir1.on(); dir2.on()
            pwm1.value = pwm2.value = speed
        elif key == ord('a'):
            dir1.off(); dir2.on() # Spin Left
            pwm1.value = pwm2.value = speed
        elif key == ord('d'):
            dir1.on(); dir2.off() # Spin Right
            pwm1.value = pwm2.value = speed
        elif key == ord(' '):
            pwm1.value = pwm2.value = 0 # Stop
        elif key == ord('q'):
            break

curses.wrapper(main)
