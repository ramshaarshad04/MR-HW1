#rclpy is a Python API for communicating and inetracting with ROS2
import rclpy

#We are sending char as messages
from std_msgs.msg import Char

#We need the Node class
from rclpy.node import Node

class PublisherNode(Node):
    def __init__(self):
    	super().__init__('node_publisher')
    
    	self.publisher_ = self.create_publisher(Char, 'user_input', 20)
    	commRate = 1
    
    	self.timer = self.create_timer(commRate, self.callbackFunction)
    	self.counter = 0
    
    def callbackFunction(self):
    	user_char = input('Enter a character: ')
    	
    	if len(user_char) != 1:
    		self.get_logger().warn('Please enter exactly one character.')
    		return
    		
    	messagePublisher = Char()
    	messagePublisher.data = ord(user_char)
    	self.publisher_.publish(messagePublisher)
    	self.get_logger().info('Publisher node is publishing: "%c"' % messagePublisher.data)
    	
def main(args=None):
    rclpy.init(args=args)
    node_publisher = PublisherNode()
    rclpy.spin(node_publisher)
    node_publisher.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
