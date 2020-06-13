from game.game_api import AEGISCore
import numpy as np

class Robobot(AEGISCore):

    def start(self):
        """
        start function is called at the beginning of the game

        Write initialization code here
        """
        print("Robot Initialized")
        self.prev_pos = self.position()

    def update(self):
        """
        update function is called every frame of the game

        Write code here to dynamically control your robot
        """
        vel = (self.position() - self.prev_pos)/self.delta_time()

        self.set_acceleration(((0,3) - vel)*3)

        self.prev_pos = self.position()