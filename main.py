import tornado.ioloop
import tornado.web
import tornado.websocket

import json
import sys
import traceback

# Catch SyntaxError. Store err until it is sent to unity client.
syntax_error = ""
try:
    from game.user_code import UserRobot
except SyntaxError as err:
    print(traceback.format_exc())
    syntax_error = err

from game.sensor_data import SensorData
from logger import Logger

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """
    Handles WebSocket connections

    Methods
    -------
    open()
        Called when websocket connection is opened
    on_message()
        Called when received message from client
    on_close()
        Called when client connection closes
    """
    _terminal = sys.stdout
    logs = []

    def check_origin(self, origin):
        print("Checking origin")
        return 1
        allowed = ["http://localhost:3000", "http://localhost:5000"]
        if origin in allowed:
            print("allowed", origin)
            return 1

    def open(self):
        if(syntax_error != ""):
            print("Syntax error!")
            self.write_message(json.dumps({"data": None, "logs": [str(syntax_error)]}), binary = True)
            tornado.ioloop.IOLoop.instance().stop()
        else:
            try:
                print("Attempting to start UserRobot")
                self.user_robot = UserRobot()
                print("WebSocket opened")
            except Exception as err:
                print(traceback.format_exc())
                self.write_message(json.dumps({"data": None, "logs": [str(err)]}), binary = True)
                tornado.ioloop.IOLoop.instance().stop()


    def on_message(self, message):
        """
        Receive and process binary data from client (unity game)

        Parameters
        ----------
        message : str (binary)
        """
        json_string = message.decode("utf-8")
        json_object = json.loads(json_string)
        game_state = SensorData(json_object)
        self.write_message(json.dumps(self.get_user_action(game_state, self.user_robot)), binary = True)

    def on_close(self):
        print("WebSocket closed")


    def get_user_action(self, game_state, user_robot):
        """
        Send new game_state to user_robot and return next action

        Parameters
        ----------
        game_state : GameState
        user_robot : UserRobot

        Returns
        -------
        dict
            {"data": {"left": ____ , "right": ____ }}
        """

        # Add new sensor data to user_robot
        user_robot.sensor_data_history += [game_state]


        # Redirect stdout to Logger object
        sys.stdout = Logger(self.logs)
     
        # Execute user code. 
        # Stdout will be logged to logs variable
        try:
            if(len(user_robot.sensor_data_history)>=3):
                if(len(user_robot.sensor_data_history)==3):
                    user_robot.start()
                user_robot.update()
        except Exception as err:
            print(traceback.format_exc())
            self.write_message(json.dumps({"data": None, "logs": [str(err)]}), binary = True)
            tornado.ioloop.IOLoop.instance().stop()

        # Switch back to terminal logger
        sys.stdout = self._terminal


        # Send data and logs to unity client
        accel = {"left": user_robot.x_acceleration, "right": user_robot.y_acceleration}
        packet = {"data": accel, "logs": self.logs}

        self.logs = []
        return packet


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()