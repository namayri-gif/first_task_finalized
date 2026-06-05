from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get the package directory
    package_dir = get_package_share_directory('my_robot_launch')
    rviz_config_path = os.path.join(package_dir, 'rviz', 'robot_config.rviz')
  
    nodes = []
  
    # Your robot nodes
    nodes.append(Node(
        package='my_robot_control',
        executable='robot_controller',
        name='robot_controller',
        output='screen'
    ))
  
    # RViz with your configuration file
    nodes.append(Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        output='screen'
    ))
  
    return LaunchDescription(nodes)
