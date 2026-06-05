from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get package directories
    my_package_dir = get_package_share_directory('my_robot_launch')
    rviz_config_file = os.path.join(my_package_dir, 'rviz', 'robot_launch.rviz')
  
    # List of nodes to launch
    nodes = [  
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
  
    return LaunchDescription(nodes)
