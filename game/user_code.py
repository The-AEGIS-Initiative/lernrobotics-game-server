from game.game_api import set_thrusters, get_position, get_sensor
import numpy as np
import time

def main():
    move_to((-2.5, 2.5))
    move_to((4.5, 2.5))

def move_to(target_pos):
    delta_time = 0.02
    prev_pos = get_position()
    delta_pos = target_pos - get_position()
    while(np.linalg.norm(delta_pos)>0.1):
        vel = (get_position() - prev_pos)/delta_time
        prev_pos = get_position()
        print(vel)
        delta_pos = target_pos - get_position()
        set_thrusters(delta_pos * 5 - 5*vel)
            
        
        

