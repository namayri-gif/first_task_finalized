import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')
  
        # Create a publisher that sends String messages to 'my_topic'
        self.publisher_ = self.create_publisher(String, 'my_topic', 10)
  
        # Create a timer to send messages every 1 second
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.counter = 0
  
    def timer_callback(self):
        # Create a message
        msg = String()
        msg.data = f'Hello World: {self.counter}'
  
        # Publish the message
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
  
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    publisher = SimplePublisher()
    rclpy.spin(publisher)
    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
