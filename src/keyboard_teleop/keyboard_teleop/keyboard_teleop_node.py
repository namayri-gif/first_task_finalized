#!/usr/bin/env python3
import sys, tty, termios, select, threading
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

LINEAR_SPEED  = 0.22
ANGULAR_SPEED = 1.5

KEY_BINDINGS = {
    'w': ( LINEAR_SPEED,  0.0),
    's': (-LINEAR_SPEED,  0.0),
    'a': ( 0.0,           ANGULAR_SPEED),
    'd': ( 0.0,          -ANGULAR_SPEED),
    '\x1b[A': ( LINEAR_SPEED,  0.0),
    '\x1b[B': (-LINEAR_SPEED,  0.0),
    '\x1b[D': ( 0.0,           ANGULAR_SPEED),
    '\x1b[C': ( 0.0,          -ANGULAR_SPEED),
}

def get_key(timeout=0.1):
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if not ready:
            return ''
        key = sys.stdin.read(1)
        if key == '\x1b':
            key += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return key

class KeyboardTeleopNode(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')
        self._pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self._timer = self.create_timer(0.1, self._publish_velocity)
        self._linear_x  = 0.0
        self._angular_z = 0.0
        self._running   = True
        threading.Thread(target=self._keyboard_loop, daemon=True).start()
        self.get_logger().info('Teleop ready! WASD/arrows=move  SPACE=stop  Q=quit')

    def _keyboard_loop(self):
        while self._running:
            key = get_key()
            if not key:
                self._linear_x = self._angular_z = 0.0
            elif key == ' ':
                self._emergency_stop()
            elif key in ('q', 'Q'):
                self._emergency_stop()
                self._running = False
                rclpy.shutdown()
            elif key in KEY_BINDINGS:
                self._linear_x, self._angular_z = KEY_BINDINGS[key]
            else:
                self._linear_x = self._angular_z = 0.0

    def _publish_velocity(self):
        msg = Twist()
        msg.linear.x  = self._linear_x
        msg.angular.z = self._angular_z
        self._pub.publish(msg)

    def _emergency_stop(self):
        self._linear_x = self._angular_z = 0.0
        self._pub.publish(Twist())
        self.get_logger().warn('EMERGENCY STOP!')

    def destroy_node(self):
        self._running = False
        self._emergency_stop()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleopNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
