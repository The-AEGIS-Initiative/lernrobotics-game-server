from game.game_api import *
import numpy as np

class UserRobot(Robot):

    def start(self):
        """
        self function is called at the beginning of the game

        Write initialization code here
        """
        print("Robot Initialized")

        self.stateMachine = FiniteStateMachine()

        moveState = MoveState(np.array([0, 0]))
        moveState2 = MoveState(np.array([0, 12.5]))

        self.stateMachine.add_transition(moveState, moveState2, moveState.isDoneMoving)
        self.stateMachine.add_transition(moveState2, moveState, moveState2.isDoneMoving)

        start_state = self.stateMachine.get_current_state()
        self.stateMachine.add_transition(start_state, moveState2, start_state.isStarted)

    def update(self):
        """
        self function is called every frame of the game

        Write code here to dynamically control your robot
        """
        self.stateMachine.next_state()
        self.stateMachine.get_current_state().do_action()


class MoveState(RobotState):
    def __init__(self, target_pos):
        super().__init__()
        self.target_pos = target_pos
    
    def do_action(self):
        self.drive_dist(self.target_pos)

    def isDoneMoving(self):
        cur_state = self.user_robot.current_sensor_data()
        return np.linalg.norm(self.calc_dist_error()) <= 0.02

    #Movement Calculation Functions
    def drive_dist(self, target_position):
        self.drive_at_vel(np.array(self.calc_dist_error()))

    def calc_dist_error(self):
        cur_state = self.user_robot.current_sensor_data()
        delta_position = self.target_pos - cur_state.position
        return delta_position

    def drive_at_vel(self, target_vel):
        vel_error = self.calc_vel_error(target_vel)
        
        self.user_robot.set_x_acceleration(vel_error[0])
        self.user_robot.set_y_acceleration(vel_error[1])
    
    def calc_vel(self):
        cur_state = self.user_robot.current_sensor_data()
        prev_state = self.user_robot.prev_sensor_data()
        
        cur_pos = cur_state.position
        prev_pos = prev_state.position
        
        delta_time = cur_state.delta_time
        vel = (cur_pos - prev_pos)/delta_time

        return vel

    def calc_vel_error(self, target_vel):
        vel = self.calc_vel()
        
        x_vel_err = target_vel[0] - vel[0]
        y_vel_err = target_vel[1] - vel[1]

        return (x_vel_err, y_vel_err)
    

"""
1) Overload different ways to access position
    - As a np vec
    - As a dict
    - As a tuple

2) Make velocity an accesible property for users?

3) Have unit test stages to accurately test methods for accuracy
"""