#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from pisense import SenseHAT

class LedDisplayEmulatorTask(BaseActuatorSimTask):
	

	def __init__(self):
		"""
        Initializes the LedDisplayEmulatorTask object.

        This constructor calls the constructor of the parent class (BaseActuatorSimTask)
        and sets up the SenseHAT emulator based on the configuration.
        """
		super( \
			LedDisplayEmulatorTask, self).__init__( \
				name = ConfigConst.LED_ACTUATOR_NAME, \
				typeID = ConfigConst.LED_DISPLAY_ACTUATOR_TYPE, \
				simpleName = "LED_Display")
		enableEmulation = \
			ConfigUtil().getBoolean( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.sh = SenseHAT(emulate = enableEmulation)

	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
        Emulates the activation of the LED Display actuator by scrolling a message on the SenseHAT LED screen.

        Args:
            val (float): The activation value to process.
            stateData (str): The string state data to use in processing the command.

        Returns:
            int: The status code indicating the result of the activation.
        """
		if self.sh.screen:
			self.sh.screen.scroll_text(stateData, size = 8)
			print('LED ON')

			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to write.")
			return -1

	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
        Emulates the deactivation of the LED Display actuator by clearing the SenseHAT LED screen.

        Args:
            val (float): The activation value to process.
            stateData (str): The string state data to use in processing the command.

        Returns:
            int: The status code indicating the result of the deactivation.
        """
		if self.sh.screen:
			self.sh.screen.clear()
			print('LED OFF')
	
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to clear / close.")
			return -1
		