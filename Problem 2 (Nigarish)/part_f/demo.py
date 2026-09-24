# import rclpy
# import math
# from rclpy.node import Node
# from geometry_msgs.msg import Twist

# topic1 = 'turtle1/cmd_vel'
# period = 0.1

# def main(args = None):
#     rclpy.init(args = args)
#     controlVel = Twist()

#     controlVel.linear.x = 2.0;
#     controlVel.linear.y = 0.0;
#     controlVel.linear.z = 0.0;

#     controlVel.angular.x = 0.0;
#     controlVel.angular.y = 0.0;
#     controlVel.angular.z = 0.8;    

#     TestNode = Node("test_node")
#     publisher = TestNode.create_publisher(Twist, topic1, 1)
#     rate = TestNode.create_rate(period)

#     while rclpy.ok():
#         print("Sending control message")
#         publisher.publish(controlVel)
#         rclpy.spin_once(TestNode)
#         rate.sleep()
    
#     TestNode.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()


import math
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

TOPIC = 'turtle1/cmd_vel'
DT = 0.1                  # seconds between publishes
Linear_Speed = 0.5
Amplitude= 1.0
Frequency = 2.0


def main(args=None):
    rclpy.init(args=args)
    node = Node('wave_motion_node')
    publisher = node.create_publisher(Twist, TOPIC, 10)

    t = 0.0
    while rclpy.ok():
        control_vel = Twist()
        control_vel.linear.x = Linear_Speed
        control_vel.linear.y = 0.0
        control_vel.linear.z = 0.0

        control_vel.angular.x = 0.0
        control_vel.angular.y = 0.0
        control_vel.angular.z = Amplitude * math.cos(Frequency * t)

        publisher.publish(control_vel)
        print(f'linear.x={control_vel.linear.x:.2f}, angular.z={control_vel.angular.z:.2f}')

        time.sleep(DT)
        t += DT
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()