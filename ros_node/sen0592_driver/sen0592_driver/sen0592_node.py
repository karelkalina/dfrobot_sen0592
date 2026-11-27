#!/usr/bin/env python3

# ROS 2 node for the DFRobot SEN0592 ultrasonic distance sensor plugged into an M5 Atom
# Lite running ESPHome. The node polls the sensor over HTTP and publishes the distance as
# a Range message.

import requests
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range

# Manufacturer specifications for the SEN0592 sensor.
MIN_RANGE_M = 0.030
MAX_RANGE_M = 5.0
FOV_RAD = 1.396  # 80°

class SEN0592Node(Node):
    def __init__(self):
        super().__init__('sen0592_node')
        self.declare_parameter('sensor_ip', '192.168.105.70')
        self.declare_parameter('frame_id', 'sen0592_link')
        self.declare_parameter('poll_period', 0.1)

        self.sensor_ip = self.get_parameter('sensor_ip').get_parameter_value().string_value
        self.frame_id = self.get_parameter('frame_id').get_parameter_value().string_value
        poll_period = self.get_parameter('poll_period').get_parameter_value().double_value

        self.url = f'http://{self.sensor_ip}/sensor/distance'
        self.publisher_ = self.create_publisher(Range, '/sen0592/range', 10)
        self.timer = self.create_timer(poll_period, self.timer_callback)

        self.get_logger().info(f'SEN0592 node started: {self.url}')

    def timer_callback(self):
        try:
            response = requests.get(self.url, timeout=(1.0, 2.0))
            response.raise_for_status()
            data = response.json()
            distance_mm = float(data['value'])
            distance_m = distance_mm / 1000.0

            msg = Range()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = self.frame_id
            msg.radiation_type = Range.ULTRASOUND
            msg.field_of_view = FOV_RAD
            msg.min_range = MIN_RANGE_M
            msg.max_range = MAX_RANGE_M
            msg.range = distance_m

            self.publisher_.publish(msg)
        except Exception as e:
            self.get_logger().warn(f'Error: {e}', throttle_duration_sec=2.0)

def main(args=None):
    rclpy.init(args=args)
    node = SEN0592Node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
