from game.game_api import AEGISCore
import numpy as np
import time

class Robobot(AEGISCore):

    def start(self):
        """
        start function is called at the beginning of the game

        Write initialization code here
        """
        pass

    def update(self):
        """
        update function is called every frame of the game

        Write code here to dynamically control your robot
        """
        self.set_acceleration(np.array((0,1)))