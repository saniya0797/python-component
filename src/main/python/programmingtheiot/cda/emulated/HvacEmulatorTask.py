#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from pisense import SenseHAT

class HvacEmulatorTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		"""
        Initializes the HvacEmulatorTask object.

        This constructor calls the constructor of the parent class (BaseActuatorSimTask)
        and sets up the SenseHAT emulator based on the configuration.
        """
		super( \
			HvacEmulatorTask, self).__init__( \
				name = ConfigConst.HVAC_ACTUATOR_NAME, \
				typeID = ConfigConst.HVAC_ACTUATOR_TYPE, \
				simpleName = "HVAC")
		enableEmulation = \
			ConfigUtil().getBoolean( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.sh = SenseHAT(emulate = enableEmulation)

	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
        Emulates the activation of the HVAC actuator by scrolling a message on the SenseHAT LED screen.

        Args:
            val (float): The activation value to process.
            stateData (str): The string state data to use in processing the command.

        Returns:
            int: The status code indicating the result of the activation.
        """
		if self.sh.screen:
			msg = self.getSimpleName() 
			print(str(val) +'HVAC On')
			self.sh.screen.scroll_text(msg)
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to write.")
			return -1

	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
        Emulates the deactivation of the HVAC actuator by scrolling a message on the SenseHAT LED screen.

        Args:
            val (float): The activation value to process.
            stateData (str): The string state data to use in processing the command.

        Returns:
            int: The status code indicating the result of the deactivation.
        """
		if self.sh.screen:
			msg = self.getSimpleName() 
			print(str(val) +'HVAC Off')
			self.sh.screen.scroll_text(msg)
			
			# optional sleep (5 seconds) for message to scroll before clearing display
			sleep(5)
			
			self.sh.screen.clear()
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to clear / close.")
			return -1