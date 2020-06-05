import numpy as np
import sys

class RobotData:
	"""
	Stores sensor data at a particular frame

	Attributes
	----------
	position : tuple
		(x,y) tuple of the robot position
	rotation : float
		angle of robot heading clockwise relative to up (north)
	forward_dir : tuple
		(x,y) unit vector indicating the forward direction of the robot
	right_dir : tuple
		(x,y) unit vector indicating the right side direction of the robot
	delta_time : float
		timestep between current frame and the previous frame in seconds
	sensor : int[]
		radial distances from the robot from 0 to 360 deg with 1 deg steps
		degrees are measured clockwise from the positive vertical axis
		ex) sensor_array[90] gives the radial distance to any object located at
		the right side of the robot


	"""
	def __init__(self, json_object):
		self.position = np.fromiter(json_object["player_position"].values(), dtype = float)
		#self.rotation = json_object["player_heading"]
		#self.forward_dir = np.fromiter(json_object["player_forward"].values(), dtype = float)
		#self.right_dir = np.fromiter(json_object["player_right"].values(), dtype = float)
		self.object_sensor = self.formatObjectSensorData(json_object)
		self.delta_time = json_object["delta_time"]
		#print(sys.getsizeof(self.object_sensor))

	def position(self):
		"""
		Return the position of the player in the currently accessed data point.
		"""
		return self.position

	def sensor(self, heading):
		"""
		Return the distance of any object in the specified angle from the forward direction of the user.

		Parameters
		----------
		heading 
			n int
			Angle representing line of sight measured clockwise from the positive vertical axis.
			i.e. Given any rotation of the robot, 0 degrees refers to the positive vertical axis.
		"""

		# Round heading to nearest multiple of 5
		canonical_angle = 5*round(heading/5)
		canonical_angle = int(canonical_angle % 360 / 5)
		
		return self.object_sensor[canonical_angle]

	def delta_time(self):
		"""
		Return the amount of time passed between the previous and the current render frame.
		"""
		return self.delta_time

	def __repr__(self):
		return (f"Position: {self.position}\n")

	#def formatObjectSensorData(self, json_object):
	#	detected_objects = json_object["object_sensor_data"]["detected_objects"]

	#	object_data = []
	#	for object in detected_objects:
	#		object_data += [GameObject(object)]

	#	return object_data

	def formatObjectSensorData(self, json_object):
		vector2_array = np.array(json_object["object_sensor_data"]["detected_objects"])
		
		res = []
		for object_info in vector2_array:
			pos = np.fromiter(object_info['position'].values(), dtype=float)
			name = object_info['name']
			res += [GameObject(pos, name)]
		return res

class GameObject():
	def __init__(self, position, name):
		# object_data_json has format 
		# {"position":{"x":0, "y":0}, "name": "example"}

		# Convert {"x":x, "y":y} to and numpy array (x, y)
		self.position = position
		self.type = name

	def __repr__(self):
		return (f"(Position: {self.position}, "
				f"Name: {self.type})\n")