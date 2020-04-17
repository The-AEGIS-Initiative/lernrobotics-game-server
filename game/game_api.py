from abc import ABC, abstractmethod
from utils.graph import Graph

class Robot(ABC):
    """
    Defines the API available to user when programming robot

    Variables
    ---------
    x_acceleration
        current acceleration in x direction
    y_acceleration
        current acceleration in y_direction
    sensor_data_history
        array of all sensor_data objects
    robot_state_history
        array of all state objects

    Methods
    -------
    start
        called once in the beginning of game
    update
        called every frame of the game
    set_left_acceleration
        Sets desired acceleration for robot
    set_right_acceleration
        Sets desired acceleration for robot
    current_robot_state
        Get the current (most recent) robot state
    prev_robot_state
        Get the previous robot state
    prev_prev_robot_state
        Get the robot state before the previous robot state
    current_sensor_data
        Get current sensor_data
    prev_sensor_data
        Get prev sensor_data
    prev_prev_sensor_data
        Get prev prev sensor data

    """
    def __init__(self):
        self.x_acceleration = 0 
        self.y_acceleration = 0
        self.sensor_data_history = []
        self.robot_state_history = []

        # Pass reference of Robot instance to RobotState
        RobotState.register_user_robot(self)


    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self):
        pass

    def set_acceleration(self, acceleration):
        """
        Sets the acceleration of the left wheel

        Parameters
        ----------
        acceleration
            (x,y) tuple
            Desired acceleration. 1 acceleration = 1 units per squared second
        """
        self.x_acceleration, self.y_acceleration = acceleration
    
    def set_x_acceleration(self, acceleration):
        """
        Sets the acceleration of the left wheel

        Parameters
        ----------
        acceleration
            float
            Desired acceleration. 1 acceleration = 1 units per squared second
        """
        self.x_acceleration = acceleration

    def set_y_acceleration(self, acceleration):
        """
        Sets the acceleration of the right wheel

        Parameters
        ----------
        acceleration
            float
            Desired acceleration. 1 acceleration = 1 units per squared second
        """
        self.y_acceleration = acceleration

    def current_sensor_data(self):
        """
        Get the current (most recent) sensor data

        Returns
        -------
        SensorData
            Most recent sensor data
        """
        return self.sensor_data_history[-1]

    def prev_sensor_data(self):
        """
        Get the previous sensor data

        Returns
        -------
        SensorData
            Previous sensor data
        """
        return self.sensor_data_history[-2]

    def prev_prev_sensor_data(self):
        """
        Get the sensor data before the previous sensor data

        Returns
        -------
        SensorData
            sensor data 2 frames ago
        """
        return self.sensor_data_history[-3]
        
    def current_robot_state(self):
        """
        Get the current (most recent) robot state data

        Returns
        -------
        RobotState
            Most recent state of the robot
            
        """
        return self.state_history[-1]

    def prev_robot_state(self):
        """
        Get the previous state history

        Returns
        -------
        RobotState
            Previous state of the robot
            
        """
        return self.state_history[-2]

    def prev_prev_robot_state(self):
        """
        Get the state history before the previous available state history

        Returns
        -------
        RobotState
            State of the robot 2 transitions ago 
            
        """
        return self.state_history[-3]


class FiniteStateMachine():
    def __init__(self):
        self.state_graph = Graph()

        # Initialize robot start state
        start_state = StartState()
        
        self.add_state(start_state)
        self.current_state = start_state
    
    def add_state(self, robot_state):
        self.state_graph.add_node(robot_state)

    def add_transition(self, start_state, end_state, condition):
        """
        Add a transition between start_state and end_state when condition is satisfied

        Parameters
        ----------
        start_state
            Origin state
        end_state
            Destination state
        condition
            Boolean function to decide when to make this transition
            condition() function takes in no arguments
        """

        # Add state if they do not exist (add_state automatically checks for existance)
        self.add_state(start_state)
        self.add_state(end_state)

        # Add transition
        self.state_graph.add_edge(start_state, end_state, condition)

    def get_current_state(self):
        return self.current_state

    def next_state(self):
        for transition in self.state_graph.graph[self.current_state]:
            end_state, condition = transition
            if(condition()):
                # Make transition and Record new state to state_history
                self.current_state = end_state
                return self.current_state
        # If all conditions are false, continue in same state
        return self.current_state

class RobotState():
    _user_robot = None

    def __init__(self):
        if(RobotState._user_robot == None):
            print("_user_robot not assigned yet!")
            return
        self.user_robot = RobotState._user_robot
        print("hew")

    def register_user_robot(user_robot):
        RobotState._user_robot = user_robot

class StartState(RobotState):
    def __init__(self):
        super().__init__()

    def isStarted(self):
        return True