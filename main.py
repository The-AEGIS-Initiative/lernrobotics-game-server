import tornado.ioloop
import tornado.web
import tornado.websocket

import threading
import os
import json
import sys
import traceback

# Save user code to file

if('code' in os.environ.keys()):
    with open("./game/user_code.py", 'w') as f:
        f.write(os.environ['code'])
else:
    print("using default test code")

# Catch SyntaxError. Store err until it is sent to unity client.
syntax_error = ""
try:
    from game.user_code import Robobot
    from game.game_api import AEGISCore
except SyntaxError as err:
    print(traceback.format_exc())
    syntax_error = err

from game.robot_data import RobotData
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
                print("Attempting to start RobobotCore")
                self.user_robot = Robobot()
                self.gameFrame = 0
                self.code_finished = False
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
        game_state = RobotData(json_object)
       
        # Add new sensor data to user_robot
        self.user_robot.robot_data_history = [game_state]

        if(self.gameFrame == 0):
            self.user_code_thread = threading.Thread(target=self.thread_wrapper)
            self.user_code_thread.start()
        self.gameFrame += 1
        # print("\n")
        # print("received response from game, triggering receivedResponseEvent")
        AEGISCore.receivedResponseEvent.set()
        if(not self.code_finished):
            AEGISCore.executedCodeEvent.wait()
            AEGISCore.executedCodeEvent.clear()
        self.write_message(json.dumps(self.get_user_action()), binary = True)

    def on_close(self):
        print("WebSocket closed")

    def thread_wrapper(self):
        self.user_robot.main()
        self.code_finished = True
        AEGISCore.lineno = -1


    def get_user_action(self):
        """
        Send new game_state to user_robot and return next action

        Parameters
        ----------
        game_state : GameState
        user_robot : RobobotCore

        Returns
        -------
        dict
            {"data": {"left": ____ , "right": ____ }}
        """

        # Redirect stdout to Logger object
        sys.stdout = Logger(self.logs)
        
        # Execute user code. 
        # Stdout will be logged to logs variable
        try:
            
            self.gameFrame += 1
        except Exception as err:
            print(traceback.format_exc())
            self.write_message(json.dumps({"data": None, "logs": [str(err)]}), binary = True)
            tornado.ioloop.IOLoop.instance().stop()

        # Switch back to terminal logger
        sys.stdout = self._terminal

        # Send data and logs to unity client
        accel = {"left": AEGISCore.x_acceleration, "right": AEGISCore.y_acceleration}
        # print("2. accelerated at (", AEGISCore.x_acceleration,",", AEGISCore.y_acceleration, ") for 0.02 seconds")
        
        packet = {"data": accel, "logs": self.logs, "lineno": AEGISCore.lineno}

        self.logs = []
        return packet


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()

    # In localhost dev environment
    if((not 'cert' in os.environ.keys()) or len(os.environ['cert'])<20):
        app.listen(8080)
    else: # In hosted development or production environment
        with open("./cert.crt", 'w') as f:
            f.write(os.environ['cert'].replace('\\n ', '\n'))
        with open('./cert.key', 'w') as f:
            f.write(os.environ['certkey'].replace('\\n ', '\n'))

        app.listen(8080, ssl_options={
            'certfile': os.path.join("./", "cert.crt"),
            'keyfile': os.path.join('./', 'cert.key')
        })
    tornado.ioloop.IOLoop.current().start()