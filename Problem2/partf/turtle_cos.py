import math
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

topic1 = '/turtle1/cmd_vel'

period = 100

def main(args=None):
    rclpy.init(args=args)
    controlVel = Twist()

    controlVel.linear.x = 1.0
    controlVel.linear.y = 0.0
    controlVel.linear.z = 0.0

    controlVel.angular.x = 0.0
    controlVel.angular.y = 0.0
    controlVel.angular.z = 0.0
    
    TestNode = Node("test_node")
    publisher = TestNode.create_publisher(Twist, topic1, 10)
    
    rate = TestNode.create_rate(period)

    amplitude = 3
    frequency = 4.0  

    start_time = time.time()

    while rclpy.ok():
        current_time = time.time() - start_time

        # Update angular velocity z dynamically 
        controlVel.angular.z = amplitude * math.cos(frequency * current_time)
        publisher.publish(controlVel)
        rclpy.spin_once(TestNode)
        rate.sleep()

    TestNode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()