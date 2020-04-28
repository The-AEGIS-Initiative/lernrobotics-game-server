from game.game_api import AEGISCore
import numpy as np

class Robobot(AEGISCore):

    def start(self):
        """
        start function is called at the beginning of the game

        Write initialization code here
        """
        print("Robot Initialized")

    def update(self):
        """
        update function is called every frame of the game

        Write code here to dynamically control your robot
        """
        self.set_acceleration((0,1))
