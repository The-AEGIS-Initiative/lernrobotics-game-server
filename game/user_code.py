from game.game_api import AEGISCore
import numpy as np

class Robobot(AEGISCore):

    def start(self):
        print("Hello")

        self.state = DecisionState()

    def update(self):
        self.set_acceleration((0.2, 1))
        #self.state.next()

class MoveState(AEGISCore):
    def __init__(self, target_pos):
        self.target_pos = target_pos
   
    def next(self):
        cur_pos = self.robot_data_history[-1].position

        if(np.linalg.norm(self.target_pos - cur_pos) < 1):
            print('transitioning to DecisionState')
            return DecisionState()
        else:
            print(self.target_pos - cur_pos)
            self.set_acceleration(self.target_pos - cur_pos)
            return MoveState(self.target_pos)

class DecisionState(AEGISCore):

    def next(self):
        next_pos = self.next_target_pos()
        print('transitioning to MoveState')
        return MoveState(next_pos)

    def next_target_pos(self):
        cur_data = self.robot_data_history[-1]
        sensor = cur_data.sensor
        cur_pos = cur_data.position

        nesw = [np.linalg.norm(np.subtract(sensor[i].name, cur_pos)) for i in (0,90,180,270)]

        return sensor[(0, 90, 180, 270)[np.argmax(nesw)]]











