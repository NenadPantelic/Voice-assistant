import serial
import time

from config.constants import SERIAL_PORT, DEFAULT_BAUD_RATE, logger


class ArduinoControlService:

    def __init__(self, port=SERIAL_PORT, baud_rate=DEFAULT_BAUD_RATE):
        self._controller = serial.Serial(port, baud_rate)
        self._state = 0

    def _state_switch(self):
        self._state = 1 - self._state

    def _turn_on(self):
        self._state = 1

    def _turn_off(self):
        self._state = 0

    def get_state(self):
        return self._state

    def _set_state(self, state_demmand):
        if state_demmand == "switch":
            self._state_switch()
        elif state_demmand == "power off":
            self._turn_off()
        elif state_demmand == "power on":
            self._turn_on()
        else:
            raise ValueError("Invalid state.")


    def _arduino_write(self):
        pass

    def control(self, state_demmand):
        print("DEBUG ",state_demmand)
        self._set_state(state_demmand)
        self._controller.write(str(self._state).encode())
        #self._arduino_write()

    def dispose(self):
        self._controller.close()


