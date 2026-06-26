#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped
import math

LINEAR_VEL = 0.22
STOP_DISTANCE = 0.5        # ← PARADA A 0.5 METROS
LIDAR_ERROR = 0.05
SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('turtlebot3_obstacle_avoidance')
        self.cmd_vel_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.get_logger().info(" Nó iniciado. Parando a 0.5m do obstáculo.")
        self.robot_moving = False

    def publish_forward(self):
        twist_stamped = TwistStamped()
        twist_stamped.header.stamp = self.get_clock().now().to_msg()
        twist_stamped.header.frame_id = 'base_link'
        twist_stamped.twist.linear.x = LINEAR_VEL
        twist_stamped.twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist_stamped)

    def publish_stop(self):
        twist_stamped = TwistStamped()
        twist_stamped.header.stamp = self.get_clock().now().to_msg()
        twist_stamped.header.frame_id = 'base_link'
        twist_stamped.twist.linear.x = 0.0
        twist_stamped.twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist_stamped)

    def scan_callback(self, scan_msg: LaserScan):
        scan_filter = self.get_front_scan(scan_msg)
        if not scan_filter:
            return
        
        min_distance = min(scan_filter)
        
        # Mostra a distância detectada
        self.get_logger().info(f' Distância: {min_distance:.2f}m | Parar se < {SAFE_STOP_DISTANCE:.2f}m')
        
        if min_distance < SAFE_STOP_DISTANCE:
            if self.robot_moving:
                self.publish_stop()
                self.robot_moving = False
                self.get_logger().info(f' PAROU! Obstáculo a {min_distance:.2f}m')
        else:
            if not self.robot_moving:
                self.publish_forward()
                self.robot_moving = True
                self.get_logger().info(f'ANDANDO... Distância: {min_distance:.2f}m')

    def get_front_scan(self, scan_msg: LaserScan):
        scan_filter = []
        samples_view = 60  # Campo de visão frontal de 60° (30° para cada lado)
        start_index = - (samples_view // 2)
        end_index = samples_view // 2
        
        for i in range(start_index, end_index + 1):
            index = i % len(scan_msg.ranges)
            distance = scan_msg.ranges[index]
            if math.isnan(distance) or math.isinf(distance):
                scan_filter.append(float('inf'))
            else:
                scan_filter.append(distance)
        return scan_filter

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Nó interrompido.")
    finally:
        node.publish_stop()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
