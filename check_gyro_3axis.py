import smbus
import time

bus = smbus.SMBus(1)
address = 0x68

# Wake up the MPU-6500 (it starts in sleep mode)
bus.write_byte_data(address, 0x6B, 0)

def read_word_2c(reg):
    high = bus.read_byte_data(address, reg)
    low = bus.read_byte_data(address, reg+1)
    val = (high << 8) + low
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

print("--- MPU-6500 XYZ Diagnostics ---")
try:
    while True:
        # Gyroscope addresses: 0x43 (X), 0x45 (Y), 0x47 (Z)
        gyro_x = read_word_2c(0x43)
        gyro_y = read_word_2c(0x45)
        gyro_z = read_word_2c(0x47)

        # Accelerometer addresses: 0x3B (X), 0x3D (Y), 0x3F (Z)
        accel_x = read_word_2c(0x3B)
        accel_y = read_word_2c(0x3D)
        accel_z = read_word_2c(0x3F)

        print(f"GYRO [deg/s]  X: {gyro_x:<6} Y: {gyro_y:<6} Z: {gyro_z:<6}")
        print(f"ACCEL [g-unit] X: {accel_x:<6} Y: {accel_y:<6} Z: {accel_z:<6}")
        print("-" * 50)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nTest Stopped.")
