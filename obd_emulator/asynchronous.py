
import time
import threading
import sys
from .obd import OBDEmulator
from .OBDResponse import OBDResponse

""" class to make asynchronous querys """
class Async(OBDEmulator):

    def __init__(self, delay_cmds=0.25, ):
        self.__thread = None
        self.__commands = {}    # key = OBDCommand, value = Response
        self.__callbacks = {}   # key = OBDCommand, value = list of Functions
        self.__running = False
        self.__was_running = False
        self.__delay_cmds = delay_cmds

    @property
    def running(self):
        return self.__running

    def start(self):
        """ Starts the async update loop """

        if len(self.__commands) == 0:
            sys.exit('Async thread not started because no commands were registered')

        if self.__thread is None:
            print("Starting async thread")
            self.__running = True
            self.__thread = threading.Thread(target=self.run)
            self.__thread.daemon = True
            self.__thread.start()

    def stop(self):
        """ Stops the async update loop """
        if self.__thread is not None:
            print("Stopping async thread...")
            self.__running = False
            self.__thread.join()
            self.__thread = None
            print("Async thread stopped")

    def paused(self):
        """
            A stub function for semantic purposes only
            enables code such as:

            with connection.paused() as was_running
                ...
        """
        return self

    def __enter__(self):
        """
            pauses the async loop,
            while recording the old state
        """
        self.__was_running = self.__running
        self.stop()
        return self.__was_running

    def __exit__(self, exc_type, exc_value, traceback):
        """
            resumes the update loop if it was running
            when __enter__ was called
        """
        if not self.__running and self.__was_running:
            self.start()

        return False  # don't suppress any exceptions

    def close(self):
        """ Closes the connection """
        self.stop()
        super(Async, self).close()

    def watch(self, c, callback=None):
        """
            Subscribes the given command for continuous updating. Once subscribed,
            query() will return that command's latest value. Optional callbacks can
            be given, which will be fired upon every new value.
        """

        # the dict shouldn't be changed while the daemon thread is iterating
        if self.__running:
            print("Can't watch() while running, please use stop()")
        else:

            # new command being watched, store the command
            if c not in self.__commands:
                print(f"Watching command: {str(c)}")

                # TODO falta implementar OBDResponse()
                self.__commands[c] = OBDResponse()  # give it an initial value
                self.__callbacks[c] = []  # create an empty list

            # if a callback was given, push it
            if hasattr(callback, "__call__") and (callback not in self.__callbacks[c]):
                print(f"subscribing callback for command: {str(c)}")
                self.__callbacks[c].append(callback)

    def unwatch(self, c, callback=None):
        """
            Unsubscribes a specific command (and optionally, a specific callback)
            from being updated. If no callback is specified, all callbacks for
            that command are dropped.
        """

        # the dict shouldn't be changed while the daemon thread is iterating
        if self.__running:
            print("Can't unwatch() while running, please use stop()")
        else:
            print(f"Unwatching command: {str(c)}")

            if c in self.__commands:
                # if a callback was specified, only remove the callback
                if hasattr(callback, "__call__") and (callback in self.__callbacks[c]):
                    self.__callbacks[c].remove(callback)

                    # if no more callbacks are left, remove the command entirely
                    if len(self.__callbacks[c]) == 0:
                        self.__commands.pop(c, None)
                else:
                    # no callback was specified, pop everything
                    self.__callbacks.pop(c, None)
                    self.__commands.pop(c, None)

    def query(self, c, force=False):
        """
            Non-blocking query().
            Only commands that have been watch()ed will return valid responses
        """

        if c in self.__commands:
            return self.__commands[c]
        else:
            return OBDResponse()

    def run(self):
        """ Daemon thread """

        # loop until the stop signal is received
        while self.__running:

            if len(self.__commands) > 0:
                # loop over the requested commands, send, and collect the response
                for c in self.__commands:

                    # force, since commands are checked for support in watch()
                    r = super(Async, self).query(c)

                    # store the response
                    self.__commands[c] = r

                    # fire the callbacks, if there are any
                    for callback in self.__callbacks[c]:
                        callback(r)
                time.sleep(self.__delay_cmds)

            else:
                time.sleep(0.25)  # idle