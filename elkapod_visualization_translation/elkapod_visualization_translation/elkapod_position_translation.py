import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import JointState
from elkapod_msgs.msg import LegFrames


class ElkapodTranslation(Node):
    def __init__(self):
        super().__init__("elkapod_translation")
        self._joint_state = [[0.0, 0.0, 0.0] for _ in range(1)]
        self._elkapod_frames_subscription = self.create_subscription(LegFrames,
                                                                     "elkapod_comm_server_leg_frames",
                                                                     self._elkapod_frames_callback,
                                                                     10)

        self._joint_state_publisher = self.create_publisher(JointState,
                                                            'joint_states',
                                                            10)
        joint_state_period = 0.03
        self._joint_state_timer = self.create_timer(joint_state_period,
                                                    self._joint_state_publish)

        # Assuming kinematic solver does not take care of this
        self.declare_parameter("hard_angle1", value=0.0)
        self.declare_parameter("hard_angle2", value=0.0)
        self.declare_parameter("hard_angle3", value=0.0)
        self._hard_angle1 = self.get_parameter("hard_angle1").get_parameter_value().double_value
        self._hard_angle2 = self.get_parameter("hard_angle2").get_parameter_value().double_value
        self._hard_angle3 = self.get_parameter("hard_angle3").get_parameter_value().double_value
        self.get_logger().info(
            f"Initialized ElkapodTranslation with hardware angles: {[self._hard_angle1, self._hard_angle2, self._hard_angle3]}"
        )

    def _elkapod_frames_callback(self, msg):
        for i, frame in enumerate(msg.leg_frames):
            if i:
                return
            else:
                # self._joint_state[i] = [np.deg2rad(el) for el in frame.servo_angles]
                self._joint_state[i][0] = np.deg2rad(frame.servo_angles[0] + self._hard_angle1)
                self._joint_state[i][1] = np.deg2rad(frame.servo_angles[1] + self._hard_angle2)
                self._joint_state[i][2] = np.deg2rad(frame.servo_angles[2] + self._hard_angle3)
                # print(self._joint_state[i])

    def _joint_state_publish(self):
        message = JointState()
        message.header.stamp = self.get_clock().now().to_msg()
        message.header.frame_id = "root"
        # For the moment there is only single leg simulation
        message.name = ['J1', 'J2', 'J3']
        # print(self._joint_state)
        message.position = self._joint_state[0]
        self._joint_state_publisher.publish(message)


def main(args=None):
    rclpy.init(args=args)
    node = ElkapodTranslation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
