import sys
sys.path.append("..")
from services.home_control.arduino_control_service import ArduinoControlService
import time

ar_s = ArduinoControlService()
for i in range(6):
    ar_s.control("switch")
    print(ar_s.get_state())
    time.sleep(3)

ar_s.control("power on")
ar_s.control("power off")
ar_s.dispose()