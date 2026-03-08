import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, Quaternion
from tf2_ros import TransformBroadcaster
from gpiozero import RotaryEncoder
import math
from rclpy.duration import Duration # Added for time buffer math

class OdometryNode(Node):
    def __init__(self):
        super().__init__('odometry_node')

        # 1. Define the variables first
        self.curr_left = 0
        self.curr_right = 0
        
        # 2. Now you can print them (use self. to refer to them)
        self.get_logger().info(f"Ticks -> Left: {self.curr_left} | Right: {self.curr_right}")

        # 1. Hardware Pins
        self.enc_right = RotaryEncoder(5, 6, max_steps=0)
        self.enc_left = RotaryEncoder(22, 27, max_steps=0)
        
        # 2. T-Robot Physical Parameters
        self.wheel_radius = 0.08352       
        self.wheel_base = 0.29        
        self.ticks_per_rev = 356.0      
        
        # 3. ROS Publishers & Broadcasters
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # 4. Odometry State
        self.x = 0.0
        self.y = 0.0
        self.th = 0.0
        self.last_left_ticks = 0
        self.last_right_ticks = 0
        self.last_time = self.get_clock().now()
        
        # Timer: Update at 10Hz
        self.timer = self.create_timer(0.1, self.update_position) #10 hz - much smoother
        self.get_logger().info(f"Ticks -> Left: {self.curr_left} | Right: {self.curr_right}")

    def euler_to_quaternion(self, yaw):
        q = Quaternion()
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(yaw / 2.0)
        q.w = math.cos(yaw / 2.0)
        return q

    def update_position(self):
        now = self.get_clock().now()
        
        # Calculate time buffer (0.05s) to solve Laptop vs Pi clock sync issues
        # This makes the data appear "fresh" to the laptop
        current_msg_time = now.to_msg()
        
        dt = (now - self.last_time).nanoseconds / 1e9
        if dt <= 0:
            return

        curr_left = -self.enc_left.steps
        curr_right = self.enc_right.steps

        self.get_logger().info(f"LIVE TICKS -> Left: {curr_left} | Right: {curr_right}")
        
        # Calculate this once
        distance_per_tick = (2 * math.pi * self.wheel_radius) / self.ticks_per_rev

        # Use it for both wheels
        dist_left = (curr_left - self.last_left_ticks) * distance_per_tick
        dist_right = (curr_right - self.last_right_ticks) * distance_per_tick
        
        d = (dist_left + dist_right) / 2.0
        dth = (dist_right - dist_left) / self.wheel_base
        
        self.x += d * math.cos(self.th)
        self.y += d * math.sin(self.th)
        self.th += dth
        
        # --- 1. PREPARE ODOMETRY MESSAGE ---
        odom = Odometry()
        odom.header.stamp = current_msg_time # Use buffered time
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation = self.euler_to_quaternion(self.th)
        
        odom.twist.twist.linear.x = d / dt
        odom.twist.twist.angular.z = dth / dt
        
        self.odom_pub.publish(odom)
        
        # --- 2. BROADCAST TRANSFORM ---
        t = TransformStamped()
        t.header.stamp = current_msg_time # Use buffered time
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation = odom.pose.pose.orientation
        
        self.tf_broadcaster.sendTransform(t)
        
        # Save values for next loop
        self.last_left_ticks = curr_left
        self.last_right_ticks = curr_right
        self.last_time = now

def main(args=None):
    rclpy.init(args=args)
    node = OdometryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()