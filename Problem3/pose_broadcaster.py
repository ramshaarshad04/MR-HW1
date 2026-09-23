import math

import numpy as np

from geometry_msgs.msg import TransformStamped

import rclpy
from rclpy.node import Node

from tf2_ros import TransformBroadcaster


def quaternion_from_euler(ai, aj, ak):
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0
    ci = math.cos(ai)
    si = math.sin(ai)
    cj = math.cos(aj)
    sj = math.sin(aj)
    ck = math.cos(ak)
    sk = math.sin(ak)
    cc = ci*ck
    cs = ci*sk
    sc = si*ck
    ss = si*sk

    q = np.empty((4, ))
    q[0] = cj*sc - sj*cs
    q[1] = cj*ss + sj*cc
    q[2] = cj*cs - sj*sc
    q[3] = cj*cc + sj*ss

    return q


def hom(angle, x=0.0, y=0.0):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s, x],
                     [s,  c, y],
                     [0.0, 0.0, 1.0]])


class FramePublisher(Node):

    def __init__(self):
        super().__init__('turtle_tf2_frame_publisher')
        self.turtlename = self.declare_parameter(
          'turtlename', 'turtle1').get_parameter_value().string_value
        if self.turtlename not in ('turtle1', 'turtle2'):
            raise ValueError("turtlename must be 'turtle1' (robot A) or 'turtle2' (robot B)")

        self.R = self.declare_parameter('R', 5.0).value           
        self.omega = self.declare_parameter('omega', 0.40).value   
        self.T = self.declare_parameter('T', 8.0).value             
        self.A = self.declare_parameter('A', 1.0).value             
        self.v = self.declare_parameter('v', 0.4).value            
        rate_hz = self.declare_parameter('rate_hz', 50.0).value
        self.t0 = self.declare_parameter('t0', 0.0).value
        self.tf_broadcaster = TransformBroadcaster(self)

        self.start = self.get_clock().now().nanoseconds * 1e-9
        self.timer = self.create_timer(1.0 / rate_hz, self.on_timer)

    def wTa(self, t):
        th = self.omega * t
        return hom(math.pi / 2 + th, self.R * math.cos(th), self.R * math.sin(th))

    def wTc(self):
        return hom(3 * math.pi / 4)

    def cTB(self, t):
        omega_t = 2 * math.pi * t / self.T
        denom = math.sqrt(4 * math.pi**2 * self.A**2 * math.cos(omega_t)**2 + self.T**2 * self.v**2)
        
        r11 = (self.T * self.v) / denom
        r12 = (-2 * math.pi * self.A * math.cos(omega_t)) / denom
        r13 = t * self.v
        
        r21 = (2 * math.pi * self.A * math.cos(omega_t)) / denom
        r22 = (self.T * self.v) / denom
        r23 = self.A * math.sin(omega_t)
        
        return np.array([[r11, r12, r13],
                         [r21, r22, r23],
                         [0.0, 0.0, 1.0]])

    def wTB(self, t):
        return self.wTc() @ self.cTB(t)

    def on_timer(self):
        now = self.get_clock().now()
        t0 = self.t0 if self.t0 > 0.0 else self.start
        t = max(0.0, now.nanoseconds * 1e-9 - t0)

        M = self.wTa(t) if self.turtlename == 'turtle1' else self.wTB(t)
        yaw = math.atan2(M[1, 0], M[0, 0])

        tf = TransformStamped()

        tf.header.stamp = now.to_msg()
        tf.header.frame_id = 'world'
        tf.child_frame_id = self.turtlename

        tf.transform.translation.x = float(M[0, 2])
        tf.transform.translation.y = float(M[1, 2])
        tf.transform.translation.z = 0.0

        q = quaternion_from_euler(0, 0, yaw)
        tf.transform.rotation.x = q[0]
        tf.transform.rotation.y = q[1]
        tf.transform.rotation.z = q[2]
        tf.transform.rotation.w = q[3]

        self.tf_broadcaster.sendTransform(tf)


def main():
    rclpy.init()
    node = FramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()
