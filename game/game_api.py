class AEGISCore:
    x_acceleration = 0.0
    y_acceleration = 0.0
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
        AEGISCore.x_acceleration, AEGISCore.y_acceleration = float(acceleration[0]), float(acceleration[1])

    def position(self):
        return self.robot_data_history[-1].position

    def delta_time(self):
        return 0.02

    def sensor(self, heading):
        return self.robot_data_history[-1].sensor(heading);
