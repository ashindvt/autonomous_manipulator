from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. RPLidar Node (The Eyes)
        # 1. RPLidar Node (Updated for stability)
        Node(
            package='rplidar_ros',
            executable='rplidar_node',
            name='rplidar_node',
            output='screen',
            parameters=[{
                'channel_type': 'serial',
                'serial_port': '/dev/ttyUSB0',
                'serial_baudrate': 115200,  # No quotes!
                'frame_id': 'laser_frame',
                'inverted': False,
                'angle_compensate': True,
                'scan_mode': 'Standard',     # This prevents the timeout
                "scan_frequency": 7.0,           # Adjust this value to control the rotation speed

                # 🔥 critical WiFi tuning
                'qos_overrides./scan.publisher.reliability': 'best_effort',
                'qos_overrides./scan.publisher.history': 'keep_last',
                'qos_overrides./scan.publisher.depth': 3,
            }]
        ),

        # 2. MPU6500 IMU Node (The Inner Ear)
        Node(
            package='mpu6500_driver',
            executable='gyro_node',
            name='gyro_node'
        ),

        # 3. Your Encoder Node (The Legs)
        Node(
            package='odometry',
            executable='encoder_node',
            name='encoder_node'
        ),

        # 4. STATIC TRANSFORMS (The Physics of your T-Shape)
        # Change these numbers based on your ruler measurements!
        # [x, y, z, yaw, pitch, roll, parent, child]
        
        # Lidar Transform
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='lidar_tf',
            arguments=['--x', '0.0', '--y', '0.0', '--z', '0.0', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'base_link', '--child-frame-id', 'laser_frame']
        ),

        # IMU Transform
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='imu_tf',
            arguments=['--x', '0.0', '--y', '0.0', '--z', '0.00', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'base_link', '--child-frame-id', 'imu_link']
        ),
    ])
