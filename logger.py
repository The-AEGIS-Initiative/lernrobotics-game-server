import sys

class Logger(object):
    def __init__(self, logs):
        self.terminal = sys.stdout
        self.logs = logs

    def write(self, message):
        self.terminal.write(message)
        self.logs += [message]

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    

