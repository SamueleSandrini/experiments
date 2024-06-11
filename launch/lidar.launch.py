# Copyright 2024 National Council of Research of Italy (CNR) - Intelligent Robotics Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    rplidar_ros = get_package_share_directory('rplidar_ros')

    namespace = os.getenv('NAMESPACE', '')

    tf_pub_cmd = Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher',
            namespace=namespace,
            arguments=['0', '0', '0.1', '3.14', '0', '0', 'base_link', 'laser'],
            remappings=[
                ('/tf_static', f'/{namespace}/tf_static')
            ]
        )
    lidar_cmd = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                rplidar_ros, '/launch/rplidar_s2_launch.py'
            ]),
            launch_arguments={'ns': namespace}.items()
    )
    # Create the launch description and populate
    ld = LaunchDescription()

    ld.add_action(tf_pub_cmd)
    ld.add_action(lidar_cmd)

    return ld
