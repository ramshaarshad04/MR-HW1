import math

import rclpy
from rclpy.node import Node

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from turtlesim.srv import Spawn, TeleportAbsolute

OFFSET = 5.544445


def yaw_from_quat(q):
    return math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                      1.0 - 2.0 * (q.y * q.y + q.z * q.z))


class FrameListener(Node):

    def __init__(self):
        super().__init__('turtle_tf2_frame_listener')

        self.world_frame = self.declare_parameter(
            'world_frame', 'world').get_parameter_value().string_value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.spawner = self.create_client(Spawn, 'spawn')
        self.turtle_spawning_service_ready = False
        self.turtle_spawned = False

        self.teleporters = {
            'turtle1': self.create_client(TeleportAbsolute, 'turtle1/teleport_absolute'),
            'turtle2': self.create_client(TeleportAbsolute, 'turtle2/teleport_absolute'),
        }

        self.timer = self.create_timer(0.02, self.on_timer)

    def on_timer(self):
        if self.turtle_spawning_service_ready:
            if self.turtle_spawned:
                for name in ('turtle1', 'turtle2'):
                    try:
                        t = self.tf_buffer.lookup_transform(
                            self.world_frame,
                            name,
                            rclpy.time.Time())
                    except TransformException as ex:
                        self.get_logger().info(
                            f'Could not transform {self.world_frame} to {name}: {ex}',
                            throttle_duration_sec=1.0)
                        continue

                    request = TeleportAbsolute.Request()
                    request.x = t.transform.translation.x + OFFSET
                    request.y = t.transform.translation.y + OFFSET
                    request.theta = yaw_from_quat(t.transform.rotation)
                    self.teleporters[name].call_async(request)
            else:
                if self.result.done():
                    self.get_logger().info(
                        f'Successfully spawned {self.result.result().name}')
                    self.turtle_spawned = True
                else:
                    self.get_logger().info('Spawn is not finished', throttle_duration_sec=1.0)
        else:
            if self.spawner.service_is_ready():
                request = Spawn.Request()
                request.name = 'turtle2'
                request.x = float(OFFSET)
                request.y = float(OFFSET)
                request.theta = float(0)
                self.result = self.spawner.call_async(request)
                self.turtle_spawning_service_ready = True
            else:
                self.get_logger().info('Service is not ready', throttle_duration_sec=1.0)


def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
