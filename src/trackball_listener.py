from datetime import datetime
import time

from src.socket import UDPSocket
from src.constants import (
    INTERFACE_ADDR,
    INTERFACE_PORT,
    TRACKBALL_ADDR,
    TRACKBALL_PORT,
    TRACKBALL_LISTENER_ADDR,
    TRACKBALL_LISTENER_PORT,
)


class TrackballListener:
    def __init__(self) -> None:
        # create UDP socket. This will be used for communication both with
        # the visualstim interface object, and with the trackball computer
        self.sock = UDPSocket(TRACKBALL_LISTENER_ADDR, TRACKBALL_LISTENER_PORT)

        # the interval (in seconds) over which speed values should be computed
        self.interval = 0.2

        # running speed threshold
        self.threshold = 100

        # lists to hold timestamps + associated speed values
        self.timestamps = []
        self.speeds = []

        # state flag - can be idle, waiting or running
        self.state = "idle"

    # helper func to get the seconds elapsed since given datetime
    def elapsed(self, dt):
        return (datetime.now() - dt).total_seconds()

    # check every 200 ms for a signal from the interface object. If we
    # get a "start" signal, then run. If we get a "stop" signal, stop waiting
    # and return to idle state
    def wait(self):
        self.state = "waiting"

        while self.state == "waiting":
            signal = self.sock.readData()

            if signal == "stop":
                self.state = "idle"
            elif signal == "start":
                self.state = "running"

            time.sleep(0.2)

        if self.state == "running":
            self._run()

    # main function - we tell the trackball computer to start recording and
    # transmitting displacement values, which we use to compute running speed
    # and send consequent commands back to the interface object
    def _run(self):
        # send start signal to trackball
        print("sending start signal")
        self.sock.sendData("start", TRACKBALL_ADDR, TRACKBALL_PORT)

        # initialise tPrev and disp
        tPrev = tStart = datetime.now()
        disp = 0

        # main loop - each iteration, we check for a "stop" signal from the interface
        # object. If we get one, we propagate it to the trackball computer and break
        # out of the loop. Otherwise, we read the next displacement value from the
        # trackball computer - if we've reached the end of another interval, then
        # we compute the running speed over the concluded interval and record it.
        # Otherwise, we add the new displacement value to the current interval's total
        while self.state == "running":
            if self.sock.readData() == "stop":
                self.state = "idle"
                print("sending stop signal")
                self.sock.sendData("stop", TRACKBALL_ADDR, TRACKBALL_PORT)

            d = self.sock.readData() or 0
            tDelta = self.elapsed(tPrev)

            if tDelta < self.interval:
                disp += int(d)
            else:
                self.timestamps.append(self.elapsed(tStart))
                self.speeds.append(disp / self.interval)
                self.processCurrentSpeed()
                tPrev, disp = datetime.now(), 0

        print(f"len(timestamps): {len(self.timestamps)}")
        print(f"len(speeds): {len(self.speeds)}")
        print(f"timestamps[:10]: {self.timestamps[:10]}")
        print(f"speeds[:10]: {self.speeds[:10]}")

    def processCurrentSpeed(self):
        # if speed has not changed, do nothing
        if len(self.speeds) < 2 or (self.speeds[-1] == self.speeds[-2]):
            return

        # otherwise, send "running" if speed reaches threshold, or "still" if not
        message = "running" if self.speeds[-1] >= self.threshold else "still"
        self.sock.sendData(message, INTERFACE_ADDR, INTERFACE_PORT)
