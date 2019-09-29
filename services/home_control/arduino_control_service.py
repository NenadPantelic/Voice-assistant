import serial
from config.config import SERIAL_PORT, DEFAULT_BAUD_RATE, logger


class ArduinoControlService:

    def __init__(self, port=SERIAL_PORT, baud_rate=DEFAULT_BAUD_RATE):
        self._controller = serial.Serial(port, baud_rate)
        self._state = 0

    # private methods
    def _state_switch(self):
        """
        Switches the output state.
        :return: void method
        """
        self._state = 1 - self._state

    def _turn_on(self):
        """
        Sets output state to high.
        :return: void method
        """
        self._state = 1

    def _turn_off(self):
        """
        Sets output state to low.
        :return: void method
        """
        self._state = 0

    def _set_state(self, state):
        """
        Sets output state based on state value.
        :param state: value that determines output state - one of the following values (`switch`, `power off`,
        `power on`) (str)
        :return: void method
        """
        if state == "switch":
            self._state_switch()
        elif state == "power off":
            self._turn_off()
        elif state == "power on":
            self._turn_on()
        else:
            raise ValueError("Invalid state.")
        logger.debug("Current relay state = {}".format(self.get_state()))

    # public methods
    def get_state(self):
        """
        Returns output state.
        :return: output state 0/1
        """
        return self._state

    def control(self, state):
        """
        Control arduino writing through serial port. Output state is written as str.
        :param state: value that determines output state - one of the following values (`switch`, `power off`,
        `power on`) (str)
        :return: void method
        """
        logger.debug("Calling arduino control method with params: [state = {}]".format(state))
        self._set_state(state)
        self._controller.write(str(self._state).encode())

    def dispose(self):
        """
        Closes the serial port.
        :return: void method
        """
        self._controller.close()
