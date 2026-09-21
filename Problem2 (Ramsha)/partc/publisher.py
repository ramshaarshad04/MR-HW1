import rclpy
from std_msgs.msg import Char
from rclpy.node import Node

class PublisherNode(Node):

    def __init__(self):

        super().__init__('node_publisher')
        self.publisher_ = self.create_publisher(
            Char, 'communication_topic', 15
        )
        commRate = 1
        self.timer = self.create_timer(commRate, self.callbackFunction)

    def callbackFunction(self):
        messagePublisher = Char()
        user_input = input('Enter a character to publish: ')
        messagePublisher.data = ord(user_input[0])
        self.publisher_.publish(messagePublisher)
        self.get_logger().info(
            'Publisher node is publishing:"%s"' % messagePublisher.data
        )

def main(args=None):
    rclpy.init(args=args)
    node_publisher = PublisherNode()
    rclpy.spin(node_publisher)
    node_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()