import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import smbus

class Mpu6500Node(Node):
    def __init__(self):
        super().__init__('mpu6500_node')
        self.publisher_ = self.create_publisher(Imu, 'imu/data', 10)
        self.timer = self.create_timer(0.1, self.timer_callback) # 10Hz
        self.bus = smbus.SMBus(1)
        self.address = 0x68
        self.bus.write_byte_data(self.address, 0x6B, 0) # Wake up

    def read_word_2c(self, reg):
        high = self.bus.read_byte_data(self.address, reg)
        low = self.bus.read_byte_data(self.address, reg+1)
        val = (high << 8) + low
        return val - 65536 if val >= 0x8000 else val

    def timer_callback(self):
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'

        # Conversion: Raw to m/s^2 (Accel) and rad/s (Gyro)
        # Note: ROS 2 uses Radians, not Degrees!

	## --- Linear Acceleration (m/s^2) ---
        # Raw value divided by 16384.0 (for 2g range) multiplied by gravity
        msg.linear_acceleration.x = self.read_word_2c(0x3B) / 16384.0 * 9.81
        msg.linear_acceleration.y = self.read_word_2c(0x3D) / 16384.0 * 9.81
        msg.linear_acceleration.z = self.read_word_2c(0x3F) / 16384.0 * 9.81

        # --- Angular Velocity (radians/s) ---
        # Raw value divided by 131.0 (for 250deg/s range) converted to Radians
        degree_to_rad = 3.14159 / 180.0
        msg.angular_velocity.x = (self.read_word_2c(0x43) / 131.0) * degree_to_rad
        msg.angular_velocity.y = (self.read_word_2c(0x45) / 131.0) * degree_to_rad
        msg.angular_velocity.z = (self.read_word_2c(0x47) / 131.0) * degree_to_rad

        # Orientation (Quaternions) - Usually calculated by a filter, set to neutral for now
        msg.orientation.w = 1.0

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing IMU data...')

def main(args=None):
    rclpy.init(args=args)
    node = Mpu6500Node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
