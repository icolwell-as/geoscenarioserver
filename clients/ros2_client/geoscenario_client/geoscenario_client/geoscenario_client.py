import rclpy
import math
from rclpy.node import Node

from geoscenario_msgs.msg import Tick, Pedestrian, Vehicle

from .SimSharedMemoryClient import *

class GSClient(Node):

    def __init__(self):
        super().__init__('geoscenario_client')
        self.tick_pub = self.create_publisher(Tick, '/gs/tick', 10)
        timer_period = 0.033333  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.sim_client_shm = SimSharedMemoryClient()


    def timer_callback(self):
        header, vehicles, pedestrians = self.sim_client_shm.read_server_state()

        # TODO: Check if we skipped a tick, etc.

        tick_msg = Tick()
        tick_msg.tick_count = header[0]
        tick_msg.delta_time = header[1]

        for vehicle in vehicles:
            msg = Vehicle()
            msg.id = vehicle["id"]
            msg.type = vehicle["type"]
            msg.position.x = vehicle["x"]
            msg.position.y = vehicle["y"]
            msg.position.z = vehicle["z"]
            msg.velocity.x = vehicle["vx"]
            msg.velocity.y = vehicle["vy"]
            msg.yaw = vehicle["yaw"] * math.pi / 180
            msg.steering_angle = vehicle["steering_angle"]
            tick_msg.vehicles.append(msg)

        for pedestrian in pedestrians:
            msg = Pedestrian()
            msg.id = pedestrian["id"]
            msg.type = pedestrian["type"]
            msg.position.x = pedestrian["x"]
            msg.position.y = pedestrian["y"]
            msg.position.z = pedestrian["z"]
            msg.velocity.x = pedestrian["vx"]
            msg.velocity.y = pedestrian["vy"]
            msg.yaw = pedestrian["yaw"] * math.pi / 180
            tick_msg.pedestrians.append(msg)

        self.tick_pub.publish(tick_msg)


def main(args=None):
    rclpy.init(args=args)

    gs_client = GSClient()

    rclpy.spin(gs_client)

    gs_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
