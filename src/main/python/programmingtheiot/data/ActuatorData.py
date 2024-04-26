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
	 ActuatorData class represents a simple actuator data command.
	
	"""

	def __init__(self, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, name = ConfigConst.NOT_SET, d = None):
		
		"""
		Call the constructor of the parent class (BaseIotData)
		initialize class-scoped variables for value, command, stateData, and isResponse.
		
		@param typeID: The type ID for the actuator (default: ConfigConst.DEFAULT_ACTUATOR_TYPE).
		@param name: The name of the actuator (default: ConfigConst.NOT_SET).
		
		"""
		
		#Call the constructor of the parent class (BaseIotData)
		super(ActuatorData, self).__init__(name = name, typeID = typeID, d = d)
		
		# Initialize class-scoped variables with default values
		self.value = ConfigConst.DEFAULT_VAL
		self.command = ConfigConst.DEFAULT_COMMAND
		self.stateData = ""
		self.isResponse = False
		pass
	
	def getCommand(self) -> int:
		
		""" 
		@return: The command value as Integer  
		"""
		
		return self.command
		pass
	
	def getStateData(self) -> str:
		 
		""" 
		@return The state data as a string. 
		"""
		
		return self.stateData
		pass
	
	def getValue(self) -> float:
		
		"""
		@return: The actuator value as a float.
		
		"""
		return self.value
		pass
	
	def isResponseFlagEnabled(self) -> bool:
		"""
		Check if the isResponse flag is enabled.

    	@return: True if the isResponse flag is enabled, False otherwise.
		"""
		return self.isResponse
	
	def setCommand(self, command: int):
		
		"""
		@param command: The command value to set as an integer.
		"""
		self.command=command
		self.updateTimeStamp()
		pass
	
	def setAsResponse(self):
		"""
		Set the isResponse flag as True.

		This indicates that the actuator data is a response.

		@return: None
		"""
		self.isResponse = True
		self.updateTimeStamp()
		pass
		
	def setStateData(self, stateData: str):
		""".
		@param:  stateData: The state data to set as a string.
		"""
		if stateData:
			self.stateData = stateData
			self.updateTimeStamp()
		pass
	
	def setValue(self, val: float):
		"""
		@param:  val: The actuator value to set as a float.
		"""
		self.value = val
		self.updateTimeStamp()
		pass
		
	def _handleUpdateData(self, data):
		
		"""
		Handle updating the ActuatorData properties from another ActuatorData object.

		@param data: The ActuatorData object to update from.
		
		"""
		if data and isinstance(data, ActuatorData):
			self.command = data.getCommand()
			self.stateData = data.getStateData()
			self.value = data.getValue()
			self.isResponse = data.isResponseFlagEnabled()
		pass
		