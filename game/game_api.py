import json
import time
import threading
import inspect

class AEGISCore():
    x_acceleration = 0.0
    y_acceleration = 0.0
    robot_data_history = []
    receivedResponseEvent = threading.Event()
    executedCodeEvent = threading.Event()
    lineno = 0;

def set_thrusters(thrusters, duration=20):
    """
    Exposed API function

    Sets the magnitude and direction of robot thrusters

    Parameters
    ----------
    force vector
        (x,y) tuple
        Applies a force of (x, y) to robot
    duration
        int
        thruster duration in seconds (s)
    """

    while(duration > 0):
        _set_acceleration(thrusters)
        #print("1. New acceleration set")

        #print("executedCodeEvent")
        AEGISCore.executedCodeEvent.set() # Trigger executed Code Event
        AEGISCore.lineno = get_line_num()

        #print("Waiting for receivedResponseEvent")
        AEGISCore.receivedResponseEvent.wait()
        AEGISCore.receivedResponseEvent.clear()
        #print("receivedResponseEvent")

        

        
        
        duration -= 0.02

def _set_acceleration(acceleration):
    """
    Internal Use Function Only

    Sets the acceleration of the left wheel

    Parameters
    ----------
    acceleration
        (x,y) tuple
        Desired acceleration. 1 acceleration = 1 units per squared second
    """
    AEGISCore.x_acceleration, AEGISCore.y_acceleration = float(acceleration[0])*30/255, float(acceleration[1])*30/255

def get_position():
    return AEGISCore.robot_data_history[-1].position # return current position

def get_prev_position():
    if(len(AEGISCore.robot_data_history) < 2):
        return AEGISCore.robot_data_history[-1].position # If no prev position, return current position

    return AEGISCore.robot_data_history[-2].position # Return prev position

def get_prev_prev_position():
    if(len(AEGISCore.robot_data_history) == 1): # If no prev position, return current position
        return AEGISCore.robot_data_history[-1].position
    if(len(AEGISCore.robot_data_history) == 2): # If no prev prev position, return prev position
        return AEGISCore.robot_data_history[-2].position

    return AEGISCore.robot_data_history[-3].position # return prev prev position
        

def get_delta_time():
    return 0.02

def get_sensor(heading):
    return AEGISCore.robot_data_history[-1].sensor(heading)

def get_line_num():
    return inspect.currentframe().f_back.f_back.f_lineno
    

class ActionStack:
    action_stack = []

    def append(action_func, params, time):
        action_stack += [action_func, params, time]

    def pop():
        return action_stack.pop(0)
