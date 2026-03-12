import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from gpiozero import PWMOutputDevice

class BaseController(Node):
    def __init__(self):
        super().__init__('base_controller')
        
        # --- 1. MDD3A Motor Setup (Your Pins) ---
        self.m1a = PWMOutputDevice(23); self.m1b = PWMOutputDevice(18) # Left
        self.m2a = PWMOutputDevice(24); self.m2b = PWMOutputDevice(19) # Right

        # --- 2. ROS Connections ---
        # Subscribes to keyboard/teleop from your PC
        self.subscription = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        
        # Timer for Odom updates (20Hz)
        self.get_logger().info("Base Controller is online and listening to /cmd_vel")

    def cmd_vel_callback(self, msg):
        # Convert Keyboard commands to Motor movements
        linear = msg.linear.x
        angular = msg.angular.z

        if linear > 0: self.forward()
        elif linear < 0: self.backward()
        elif angular > 0: self.left()
        elif angular < 0: self.right()
        else: self.stop()

    # --- Motor Pin Logic ---
    def stop(self):
        self.m1a.value = 0; self.m1b.value = 0
        self.m2a.value = 0; self.m2b.value = 0

    def forward(self):
        self.m1a.value = 0; self.m1b.value = 0.5
        self.m2a.value = 0; self.m2b.value = 0.5

    def backward(self):
        self.m1a.value = 0.5; self.m1b.value = 0
        self.m2a.value = 0.5; self.m2b.value = 0

    def right(self):
        self.m1a.value = 0.5; self.m1b.value = 0
        self.m2a.value = 0; self.m2b.value = 0.5

    def left(self):
        self.m1a.value = 0; self.m1b.value = 0.5
        self.m2a.value = 0.5; self.m2b.value = 0

def main():
    rclpy.init()
    node = BaseController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
