class AEGISCore:
    x_acceleration = 0
    y_acceleration = 0
    robot_data_history = []
    """
    Defines the API available to user when programming robot

    Variables
    ---------
    x_acceleration
        current acceleration in x direction
    y_acceleration
        current acceleration in y_direction
    robot_data_history
        array of all sensor_data objects

    Methods
    -------
    set_acceleration
        Sets desired acceleration for robot
    """

    def set_acceleration(self, acceleration):
        """
        Sets the acceleration of the left wheel

        Parameters
        ----------
        acceleration
            (x,y) tuple
            Desired acceleration. 1 acceleration = 1 units per squared second
        """
        AEGISCore.x_acceleration, AEGISCore.y_acceleration = acceleration


    def robot_data_history(self, time):
        return AEGISCore.robot_data_history[time]