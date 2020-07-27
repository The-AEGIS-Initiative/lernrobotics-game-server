from game.game_api import set_thrusters, get_position, get_prev_position, get_prev_prev_position, get_sensor
import numpy as np
import time

def main():
    move_to((-2.5, 2.5))
    move_to((4.5, 2.5))

def move_to(target_pos):
    delta_time = 0.02
    delta_pos = target_pos - get_position()
    while(np.linalg.norm(delta_pos)>0.1):
        vel = (get_position() - get_prev_position())/delta_time
        print("vel", vel)
        print("position", get_position())
        print("prev position", get_prev_position())
        print("prev prev position", get_prev_prev_position())
        delta_pos = target_pos - get_position()
        set_thrusters(delta_pos * 5 - 5*vel)
            
        
        

