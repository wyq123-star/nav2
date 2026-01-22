# 在你的 launch.py 中
from launch_ros.actions import Node

# 1. 静态发布 map -> odom (假设它们重合)
Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    arguments = ['0', '0', '0', '0', '0', '0', 'map', 'odom']
),

# 2. 静态发布 odom -> base_link (通常不用静态，除非是测试)
Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    arguments = ['0', '0', '0', '0', '0', '0', 'odom', 'base_link']
),
