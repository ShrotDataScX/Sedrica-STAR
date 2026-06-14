#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from part2_navigation_modules.tb3_tools import quaternion_to_euler
from math import sqrt, pow, pi


class Square(Node):

    def __init__(self):
        super().__init__("move_square")

        self.first_message = False
        self.turn = False
        self.shutdown = False

        self.vel_msg = Twist()

        self.x = 0.0
        self.y = 0.0
        self.theta_z = 0.0

        self.xref = 0.0
        self.yref = 0.0
        self.theta_zref = 0.0

        self.side_count = 0
        self.loop_count = 0

        self.vel_pub = self.create_publisher(
            msg_type=Twist,
            topic="/cmd_vel",
            qos_profile=10,
        )

        self.odom_sub = self.create_subscription(
            msg_type=Odometry,
            topic="/odom",
            callback=self.odom_callback,
            qos_profile=10,
        )

        ctrl_rate = 10
        self.timer = self.create_timer(
            timer_period_sec=1 / ctrl_rate,
            callback=self.timer_callback,
        )

        self.get_logger().info(
            f"The '{self.get_name()}' node is initialised."
        )

    def on_shutdown(self):
        self.get_logger().info("Stopping the robot...")
        self.vel_pub.publish(Twist())
        self.shutdown = True

    def odom_callback(self, msg_data: Odometry):
        pose = msg_data.pose.pose

        roll, pitch, yaw = quaternion_to_euler(pose.orientation)

        self.x = pose.position.x
        self.y = pose.position.y
        self.theta_z = yaw

        if not self.first_message:
            self.first_message = True
            self.xref = self.x
            self.yref = self.y
            self.theta_zref = self.theta_z

    def angle_difference(self, current, reference):
        diff = current - reference

        while diff > pi:
            diff -= 2 * pi

        while diff < -pi:
            diff += 2 * pi

        return abs(diff)

    def timer_callback(self):
        if not self.first_message:
            return

        if self.loop_count >= 2:
            self.vel_msg.linear.x = 0.0
            self.vel_msg.angular.z = 0.0
            self.vel_pub.publish(self.vel_msg)
            self.get_logger().info("Completed two square loops. Robot stopped.")
            return

        displacement = sqrt(
            pow(self.x - self.xref, 2) + pow(self.y - self.yref, 2)
        )

        if self.turn:
            angle_turned = self.angle_difference(self.theta_z, self.theta_zref)

            if angle_turned < pi / 2:
                self.vel_msg.linear.x = 0.0
                self.vel_msg.angular.z = 0.3
            else:
                self.vel_msg.linear.x = 0.0
                self.vel_msg.angular.z = 0.0

                self.turn = False
                self.xref = self.x
                self.yref = self.y
                self.theta_zref = self.theta_z

                self.side_count += 1

                if self.side_count == 4:
                    self.side_count = 0
                    self.loop_count += 1
                    self.get_logger().info(
                        f"Completed loop {self.loop_count}/2"
                    )

        else:
            if displacement < 1.0:
                self.vel_msg.linear.x = 0.1
                self.vel_msg.angular.z = 0.0
            else:
                self.vel_msg.linear.x = 0.0
                self.vel_msg.angular.z = 0.0

                self.turn = True
                self.theta_zref = self.theta_z

        self.vel_pub.publish(self.vel_msg)


def main(args=None):
    rclpy.init(
        args=args,
        signal_handler_options=SignalHandlerOptions.NO,
    )

    move_square = Square()

    try:
        rclpy.spin(move_square)

    except KeyboardInterrupt:
        print(
            f"{move_square.get_name()} received a shutdown request (Ctrl+C)."
        )

    finally:
        move_square.on_shutdown()

        while not move_square.shutdown:
            continue

        move_square.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()