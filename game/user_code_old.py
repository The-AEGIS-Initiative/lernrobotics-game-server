from game.game_api import GameAPI

class UserRobot(GameAPI):
	left = 0
	right = 0

	forward_dist = 0

	dist = 0

	actions = ["up", "right", "down"]

	cur_action = actions[0]
	cur_index = 0

	def start(self):
		"""
		self function is called at the beginning of the game

		Write initialization code here
		"""
		print("Robot Initialized")
		self.dist = self.get_current_state().sensor_array[0]
		#print(self.dist)
		self.finished = False

	def update(self):
		"""
		self function is called every frame of the game

		Write code here to dynamically control your robot
		"""
		

		if(not self.finished):
			self.finished = self.move(self.dist, self.cur_action)
		if(self.finished):
			self.cur_index += 1
			self.cur_action = self.actions[self.cur_index]
			self.finished = False
			

	def move(self, target_dist, direction):
		#print(direction)
		cur_state = self.get_current_state()
		dist = 0
		if(direction == "up"):
			dist = cur_state.sensor_array[0]
		elif(direction == "right"):
			dist = cur_state.sensor_array[90]
		elif(direction == "down"):
			dist = cur_state.sensor_array[180]
		elif(direction == "left"):
			dist = cur_state.sensor_array[270]

		#print("dist", dist)
		
		a = 0
		if(dist >= target_dist/2):
			a = self.speedError(3)
		else:
			a = self.speedError(0)

		if(direction == "up"):
			self.set_x_acceleration(0)
			self.set_y_acceleration(a)
		elif(direction == "right"):
			self.set_x_acceleration(a)
			self.set_y_acceleration(0)
		elif(direction == "down"):
			self.set_x_acceleration(0)
			self.set_y_acceleration(-a)
		elif(direction == "left"):
			self.set_x_acceleration(-a)
			self.set_y_acceleration(0)

		return dist < 2.5
	def speedError(self, target):
		state = self.get_current_state()
		prev_state = self.get_prev_state()
		x2 = (state.position['x'] - prev_state.position['x'])**2
		y2 = (state.position['y'] - prev_state.position['y'])**2
		delta_dist = (x2+y2)**(0.5)
		#print(delta_dist)
		#print(state.delta_time)
		#print(delta_dist/state.delta_time)
		#print("target", target)

		return target - delta_dist/state.delta_time
