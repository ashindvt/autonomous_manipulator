from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. Start your Gyro Node
        Node(
            package='mpu6500_driver',
            executable='gyro_node',
            name='mpu6500_node'
        ),
        # 2. Start the RPLIDAR Node (from system path)
        Node(
            package='rplidar_ros',
            executable='rplidar_composition',
            output='screen',
            parameters=[{
                'serial_port': '/dev/ttyUSB0', # Check if yours is USB0 or USB1
                'frame_id': 'laser_frame',
                'angle_compensate': True,
                'scan_mode': 'Standard'
            }]
        ),
        # 3. Static Transform (Tells ROS where the laser is compared to the robot)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0.1', '0', '0', '0', 'base_link', 'laser_frame']
        )
    ])
