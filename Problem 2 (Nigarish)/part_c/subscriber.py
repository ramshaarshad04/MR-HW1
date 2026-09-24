import rclpy
from std_msgs.msg import Char
from rclpy.node import Node

class SubscriberNode(Node):
    def __init__(self):
    	super().__init__('node_subscriber')
    	self.subscription = self.create_subscription(Char, 'user_input', self.callbackFunction, 20)
    	
    def callbackFunction(self, message):
    	self.get_logger().info('We received: "%c"' % message.data)
    	
def main(args=None):
	rclpy.init(args=args)
	node_subscriber = SubscriberNode()
	rclpy.spin(node_subscriber)
	node_subscriber.destroy_node()
	rclpy.shutdown()
	
if __name__ == '__main__':
    main()
