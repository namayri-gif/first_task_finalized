from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    nodes = []
  
    # Node 1: Robot Driver
    nodes.append(Node(
        package='my_robot_driver',
        executable='motor_controller',
        name='motor_controller',
        output='screen'
    ))
  
    # Node 2: Sensor Reader
    nodes.append(Node(
        package='my_robot_driver',
        executable='sensor_reader',
        name='sensor_reader',
        output='screen'
    ))
  
    # Node 3: Main Robot Controller
    nodes.append(Node(
        package='my_robot_control',
        executable='robot_controller',
        name='robot_controller',
        output='screen'
    ))
  
    return LaunchDescription(nodes)