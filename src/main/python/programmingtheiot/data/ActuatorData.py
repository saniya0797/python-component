#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.BaseIotData import BaseIotData

class ActuatorData(BaseIotData):
	"""
    Represents actuator data, extending the BaseIotData class.
    This class provides a shell for student implementation.
    """

	def __init__(self, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, name = ConfigConst.NOT_SET, d = None):
		"""
        Constructor for ActuatorData class.
        
        @param typeID The type ID of the actuator data.
        @param name The name of the actuator data.
        @param d The data dictionary containing additional attributes.
        """
		super(ActuatorData, self).__init__(name = name, typeID = typeID, d = d)
		self.value = ConfigConst.DEFAULT_VAL
		self.command = ConfigConst.DEFAULT_COMMAND
		self.stateData = None
		self.isResponse = False
		
	def getCommand(self) -> int:
		"""
        Gets the command associated with the actuator data.
        
        @return int The command value.
        """
		return self.command
	
	def getStateData(self) -> str:
		"""
        Gets the state data associated with the actuator data.
        
        @return str The state data.
        """
		return self.stateData
	
	def getValue(self) -> float:
		"""
        Gets the value associated with the actuator data.
        
        @return float The value.
        """
		return self.value

	
	def isResponseFlagEnabled(self) -> bool:
		"""
        Checks if the actuator data is marked as a response.
        
        @return bool True if the actuator data is marked as a response, False otherwise.
        """
		return self.isResponse
	
	def setCommand(self, command: int):
		"""
        Sets the command associated with the actuator data.
        
        @param command The command value to set.
        """
		self.command = command
		self.updateTimeStamp()
	
	def setAsResponse(self):
		"""
        Marks the actuator data as a response.
        """
		self.isResponse = True
		self.updateTimeStamp()
		
	def setStateData(self, stateData: str):
		"""
        Sets the state data associated with the actuator data.
        
        @param stateData The state data to set.
        """
		if stateData:
			self.stateData = stateData
			self.updateTimeStamp()
	
	def setValue(self, val: float):
		"""
        Sets the value associated with the actuator data.
        
        @param val The value to set.
        """
		self.value = val
		self.updateTimeStamp()
		
	def _handleUpdateData(self, data):
		"""
        Handles the update of actuator data attributes based on another ActuatorData instance.
        
        @param data The ActuatorData instance to use for the update.
        """
		if data and isinstance(data, ActuatorData):
			self.command = data.getCommand()
			self.stateData = data.getStateData()
			self.value = data.getValue()
			self.isResponse = data.isResponseFlagEnabled()

	