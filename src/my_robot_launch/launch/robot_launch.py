from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get package directories
    my_package_dir = get_package_share_directory('my_robot_launch')
    rviz_config_file = os.path.join(my_package_dir, 'rviz', 'main_view.rviz')
  
    # List of nodes to launch
    nodes = [
        # Your robot's motor controller
        Node(
            package='my_robot_driver',
            executable='motor_controller',
            name='motor_controller',
            output='screen',
            parameters=[
                {'max_speed': 1.0},
                {'max_acceleration': 0.5}
            ]
        ),
  
        # Your robot's sensor reader
        Node(
            package='my_robot_driver',
            executable='sensor_reader',
            name='sensor_reader',
            output='screen'
        ),
  
        # Main robot controller
        Node(
            package='my_robot_control',
            executable='main_controller',
            name='main_controller',
            output='screen',
            remappings=[
                ('cmd_vel', '/robot/cmd_vel')
            ]
        ),
  
        # TF2 broadcaster from external package
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_tf',
            arguments=['0', '0', '0.1', '0', '0', '0', 'base_link', 'laser_link'],
            output='screen'
        ),
  
        # RViz visualization
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            output='screen'
        )
    ]
  
    return LaunchDescription(nodes)