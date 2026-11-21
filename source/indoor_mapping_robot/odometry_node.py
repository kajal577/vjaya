#!/usr/bin/env python3
"""Encoder odometry for single-channel wheel encoders; publishes /odom and odom->base_link."""
import math
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, Twist
from tf2_ros import TransformBroadcaster
from gpiozero import DigitalInputDevice
from . import config

class OdomNode(Node):
    def __init__(self):
        super().__init__('encoder_odometry')
        self.left_count = 0; self.right_count = 0
        self.left_sign = 1; self.right_sign = 1
        self.left_last = 0; self.right_last = 0
        self.x = 0.0; self.y = 0.0; self.yaw = 0.0
        self.left_enc = DigitalInputDevice(config.LEFT_ENCODER_A, pull_up=True)
        self.right_enc = DigitalInputDevice(config.RIGHT_ENCODER_A, pull_up=True)
        self.left_enc.when_activated = self.left_tick
        self.right_enc.when_activated = self.right_tick
        self.cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.command_direction, 10)
        self.pub = self.create_publisher(Odometry, '/odom', 20)
        self.tf = TransformBroadcaster(self)
        self.timer = self.create_timer(0.05, self.update)
        self.last_time = self.get_clock().now()
        self.get_logger().warn('Odometry uses single-channel encoders and commanded direction; tune counts/rev and wheel dimensions.')

    def command_direction(self, msg):
        left_v = msg.linear.x - msg.angular.z * config.WHEEL_BASE_M / 2.0
        right_v = msg.linear.x + msg.angular.z * config.WHEEL_BASE_M / 2.0
        self.left_sign = 1 if left_v >= 0 else -1
        self.right_sign = 1 if right_v >= 0 else -1

    def left_tick(self): self.left_count += self.left_sign
    def right_tick(self): self.right_count += self.right_sign

    def update(self):
        now = self.get_clock().now()
        dt = max((now - self.last_time).nanoseconds / 1e9, 1e-4)
        dl_count = self.left_count - self.left_last
        dr_count = self.right_count - self.right_last
        self.left_last = self.left_count; self.right_last = self.right_count
        distance_per_count = math.pi * config.WHEEL_DIAMETER_M / config.ENCODER_COUNTS_PER_WHEEL_REV
        dl = dl_count * distance_per_count; dr = dr_count * distance_per_count
        ds = (dl + dr) / 2.0; dtheta = (dr - dl) / config.WHEEL_BASE_M
        self.x += ds * math.cos(self.yaw + dtheta / 2.0)
        self.y += ds * math.sin(self.yaw + dtheta / 2.0)
        self.yaw = math.atan2(math.sin(self.yaw + dtheta), math.cos(self.yaw + dtheta))
        qz = math.sin(self.yaw / 2.0); qw = math.cos(self.yaw / 2.0)
        odom = Odometry(); odom.header.stamp = now.to_msg(); odom.header.frame_id = 'odom'; odom.child_frame_id = 'base_link'
        odom.pose.pose.position.x = self.x; odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.z = qz; odom.pose.pose.orientation.w = qw
        odom.twist.twist.linear.x = ds / dt; odom.twist.twist.angular.z = dtheta / dt
        self.pub.publish(odom)
        tr = TransformStamped(); tr.header = odom.header; tr.child_frame_id = 'base_link'
        tr.transform.translation.x = self.x; tr.transform.translation.y = self.y
        tr.transform.rotation.z = qz; tr.transform.rotation.w = qw
        self.tf.sendTransform(tr); self.last_time = now

    def destroy_node(self):
        self.left_enc.close(); self.right_enc.close(); super().destroy_node()

def main(args=None):
    rclpy.init(args=args); node = OdomNode()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.destroy_node(); rclpy.shutdown()
