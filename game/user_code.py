from game.game_api import AEGISCore
import numpy as np
import time

class Robobot(AEGISCore):
    def main(self):
        self.move_to((-2.5, 2.5))
        self.move_to((4.5, 2.5))

    def move_to(self, target_pos):
        delta_time = 0.02
        prev_pos = self.position()
        delta_pos = target_pos - self.position()
        while(np.linalg.norm(delta_pos)>0.1):
            vel = (self.position() - prev_pos)/delta_time
            prev_pos = self.position()
            print(vel)
            delta_pos = target_pos - self.position()
            self.set_thrusters(delta_pos * 5 - 5*vel)
            
        
        

