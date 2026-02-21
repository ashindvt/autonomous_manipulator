from gpiozero import RotaryEncoder
from time import sleep

# Define the pins based on our plan
# Motor 1 (Right): Phase A=GPIO 5, Phase B=GPIO 6
encoder_right = RotaryEncoder(5, 6, max_steps=0)

# Motor 2 (Left): Phase A=GPIO 22, Phase B=GPIO 27
encoder_left = RotaryEncoder(22, 27, max_steps=0)

print("--- Encoder Test Started ---")
print("Spin the wheels manually and watch the numbers change.")
print("Press Ctrl+C to stop.")

try:
    while True:
        # .steps gives you the current 'count' of the encoder
        print(f"Right Wheel: {encoder_right.steps} | Left Wheel: {encoder_left.steps}")
        sleep(0.1)  # Refresh every 100ms
except KeyboardInterrupt:
    print("\nTest stopped by user.")
