from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    nodes = []
  
    # Robot controller with parameters
    nodes.append(Node(
        package='my_robot_control',
        executable='robot_controller',
        name='robot_controller',
        output='screen',
        parameters=[
            {'max_speed': 1.0},
            {'wheel_radius': 0.05},
            {'base_width': 0.3},
            {'debug_mode': True}
        ]
    ))
  
    # Sensor fusion with remapped topics
    nodes.append(Node(
        package='sensor_fusion',
        executable='fusion_node',
        name='sensor_fusion',
        output='screen',
        remappings=[
            ('imu_topic', '/robot1/imu'),
            ('odom_topic', '/robot1/odometry')
        ]
    ))
  
    return LaunchDescription(nodes)