import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimpleSubscriber(Node):
    def __init__(self):
        super().__init__('simple_subscriber')
  
        # Create a subscriber that listens to 'my_topic'
        self.subscription = self.create_subscription(
            String,
            'my_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
  
    def listener_callback(self, msg):
        # This function runs every time a message is received
        self.get_logger().info(f'I received: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    subscriber = SimpleSubscriber()
    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    

