#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class ActuatorAdapterManager(object):
	
	def __init__(self, dataMsgListener: IDataMessageListener = None):
		"""
        Initializes the ActuatorAdapterManager object.

        This constructor sets up configuration and initializes environmental actuation tasks.
        """
		self.dataMsgListener = dataMsgListener

		self.useEmulator = True
		self.useSimulator = True

		self.configUtil = ConfigUtil()
		
		self.useSimulator = \
			self.configUtil.getBoolean( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_SIMULATOR_KEY)
		self.useEmulator  = \
			self.configUtil.getBoolean( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_EMULATOR_KEY)
		self.deviceID     = \
			self.configUtil.getProperty( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		self.locationID   = \
			self.configUtil.getProperty( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		self.humidifierActuator = None
		self.hvacActuator       = None
		self.ledDisplayActuator = None

		self._initEnvironmentalActuationTasks()
	
	def _initEnvironmentalActuationTasks(self):
		"""
        Initializes environmental actuation tasks based on configuration.
        """
		if not self.useEmulator:
			self.humidifierActuator = HumidifierActuatorSimTask()

		
		# create the HVAC actuator
			self.hvacActuator = HvacActuatorSimTask()
			

		else:
			hueModule = import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask', 'HumidiferEmulatorTask')
			hueClazz = getattr(hueModule, 'HumidifierEmulatorTask')
			self.humidifierActuator = hueClazz()
			
			# create the HVAC actuator emulator
			hveModule = import_module('programmingtheiot.cda.emulated.HvacEmulatorTask', 'HvacEmulatorTask')
			hveClazz = getattr(hveModule, 'HvacEmulatorTask')
			self.hvacActuator = hveClazz()
			
			# create the LED display actuator emulator
			leDisplayModule = import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask', 'LedDisplayEmulatorTask')
			leClazz = getattr(leDisplayModule, 'LedDisplayEmulatorTask')
			self.ledDisplayActuator = leClazz()


	
	def setDataMessageListener(self, listener: IDataMessageListener=None) :
		"""
        Sets the data message listener for handling actuation messages.

        Args:
            listener (IDataMessageListener): An instance of the IDataMessageListener.

        Returns:
            bool: True if the listener is set successfully, False otherwise.
        """
		if listener:
			self.dataMsgListener = listener

	def sendActuatorCommand(self, data: ActuatorData=None) -> bool:
		"""
        Sends an actuator command and processes the actuation event.

        Args:
            data (ActuatorData): An instance of ActuatorData representing the actuator command.

        Returns:
            ActuatorData: An instance of ActuatorData representing the actuator response.
        """

		
		if data and not data.isResponseFlagEnabled():
			if data.getLocationID() == self.locationID:
				logging.info("Actuator command received for location ID %s. Processing...", str(data.getLocationID()))
				
				aType = data.getTypeID()
				responseData = None
				
				if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierActuator:
					responseData = self.humidifierActuator.updateActuator(data)
				elif aType == ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacActuator:
					responseData = self.hvacActuator.updateActuator(data)
					
					responseData = self.ledDisplayActuator.updateActuator(data)
				else:
					logging.warning("No valid actuator type. Ignoring actuation for type: %s", data.getTypeID())

				return responseData
			else:
				logging.warning("Location ID doesn't match. Ignoring actuation: (me) %s != (you) %s", str(self.locationID), str(data.getLocationID()))
		else:
			logging.warning("Actuator request received. Message is empty or response. Ignoring.")
		
		return False
	
	def startManager(self) -> bool:
		"""
		Starts the manager. This simply registers the current actuator state and - depending on
		the configuration - may activate the actuator command listeners.
		
		@return bool True on success; False otherwise
		"""
		return True
	
	def stopManager(self) -> bool:
		"""
		Stops the manager. Currently does nothing.
		
		@return bool True on success; False otherwise
		"""
		return True
	

