uint16 id
string type

# State
geometry_msgs/Point position          # [m, m, m], in local cartesian frame defined by the element 'origin'
geometry_msgs/Vector3 velocity        # [m/s]
float64 yaw                           # [rad], CCW from east
float64 steering_angle                # [rad]
bool active                           # provided only by the client to the server
