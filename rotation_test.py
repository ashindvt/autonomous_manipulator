#!/usr/bin/env python3
"""
ROTATION DIAGNOSTIC
===================
1. Run this script on your Pi
2. Drive the robot with teleop in another terminal
3. Press J (left turn) and L (right turn)
4. Script will tell you EXACTLY which fix to apply
"""

from gpiozero import RotaryEncoder
import time

enc_right = RotaryEncoder(5, 6, max_steps=0)
enc_left  = RotaryEncoder(22, 27, max_steps=0)

print("=" * 60)
print("Spin robot LEFT in place (J key) for 2 seconds then stop")
print("=" * 60)
input("Press ENTER when ready, then press J for 2 seconds...")

enc_left.steps = 0
enc_right.steps = 0
time.sleep(2.5)

l = enc_left.steps
r = enc_right.steps

print(f"\nAfter LEFT turn (J):  Left={l:+d}  Right={r:+d}")

# Diagnose
if l < 0 and r > 0:
    print("✅ Encoders correct: Left went -, Right went +")
    print("   FIX → dth = (dist_right - dist_left) / self.wheel_base")
elif l > 0 and r < 0:
    print("⚠️  Encoders swapped: Left went +, Right went -")
    print("   FIX → dth = (dist_left - dist_right) / self.wheel_base")
elif l < 0 and r < 0:
    print("⚠️  Both went negative")
    print("   FIX → negate RIGHT:  curr_right = -self.enc_right.steps")
    print("         then use:       dth = (dist_right - dist_left) / self.wheel_base")
elif l > 0 and r > 0:
    print("⚠️  Both went positive")
    print("   FIX → negate LEFT:   curr_left = -self.enc_left.steps")
    print("         then use:       dth = (dist_right - dist_left) / self.wheel_base")
elif l == 0 and r == 0:
    print("❌ No ticks detected! Check wiring or pins 5,6,22,27")
else:
    print(f"⚠️  Unexpected: only one encoder moved")

print()
print("=" * 60)
print("Now spin robot RIGHT in place (L key) for 2 seconds then stop")
print("=" * 60)
input("Press ENTER when ready, then press L for 2 seconds...")

enc_left.steps = 0
enc_right.steps = 0
time.sleep(2.5)

l2 = enc_left.steps
r2 = enc_right.steps

print(f"\nAfter RIGHT turn (L): Left={l2:+d}  Right={r2:+d}")

if l2 > 0 and r2 < 0:
    print("✅ RIGHT turn encoders correct: Left went +, Right went -")
elif l2 < 0 and r2 > 0:
    print("⚠️  RIGHT turn reversed: Left went -, Right went +  (enc labels physically swapped)")
    print("   FIX → swap pin numbers:")
    print("         self.enc_right = RotaryEncoder(22, 27, max_steps=0)")
    print("         self.enc_left  = RotaryEncoder(5, 6, max_steps=0)")

print()
print("=" * 60)
print("SUMMARY: Apply the fix shown above to odometry_node.py")
print("=" * 60)