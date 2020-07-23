import json
import time
import threading
import inspect

class AEGISCore:
    x_acceleration = 0.0
    y_acceleration = 0.0
    robot_data_history = []
    time = 0
    receivedResponseEvent = threading.Event()
    executedCodeEvent = threading.Event()
    ws = None;
    lineno = 0;

    def set_thrusters(self, thrusters, duration=20):
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
            thruster duration in milliseconds (ms)
        """

        while(duration > 0):
            # print("Pausing code execution until a response is received")
            AEGISCore.lineno = self.get_line_num()
            AEGISCore.receivedResponseEvent.wait()
            AEGISCore.receivedResponseEvent.clear()
            
            # print("Continuing code execution")

            self._set_acceleration(thrusters)
            # print("1. New acceleration set")
            AEGISCore.executedCodeEvent.set() # Trigger executed Code Event

            duration -= 20

    def _set_acceleration(self, acceleration):
        """
        Internal Use Function Only

        Sets the acceleration of the left wheel

        Parameters
        ----------
        acceleration
            (x,y) tuple
            Desired acceleration. 1 acceleration = 1 units per squared second
        """
        AEGISCore.x_acceleration, AEGISCore.y_acceleration = float(acceleration[0]), float(acceleration[1])

    def position(self):
        return self.robot_data_history[-1].position

    def delta_time(self):
        return 0.02

    def sensor(self, heading):
        return self.robot_data_history[-1].sensor(heading)

    def get_line_num(self):
        return inspect.currentframe().f_back.f_back.f_lineno

class ActionStack:
    action_stack = []

    def append(action_func, params, time):
        action_stack += [action_func, params, time]

    def pop():
        return action_stack.pop(0)
