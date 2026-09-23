import time

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    t0 = time.time() + 4.0
    common = {'t0': t0, 'A': 1.0, 'v': 0.4}  

    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='sim'),
        Node(package='learning_tf2_py', executable='pose_broadcaster', name='broadcaster1',
             parameters=[{'turtlename': 'turtle1', **common}]),
        Node(package='learning_tf2_py', executable='pose_broadcaster', name='broadcaster2',
             parameters=[{'turtlename': 'turtle2', **common}]),
        Node(package='learning_tf2_py', executable='pose_listener', name='listener'),
    ])
