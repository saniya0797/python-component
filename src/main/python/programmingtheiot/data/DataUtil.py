#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

from json import JSONEncoder
import json
import logging
import json

from decimal import Decimal
from json import JSONEncoder
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DataUtil():
	

	def __init__(self, encodeToUtf8 = False):
		"""
		Constructor for DataUtil class.
		Initializes class variables and logs the creation of the DataUtil instance.
		"""
		self.encodeToUtf8 = encodeToUtf8
		
		logging.info("Created DataUtil instance.")
	
	def actuatorDataToJson(self, data: ActuatorData = None, useDecForFloat: bool = False):
		"""
		Converts ActuatorData object to JSON format.
		
		@param data: The ActuatorData object to be converted.
		@param useDecForFloat: A flag to use Decimal for floating-point numbers in JSON.

		@return: JSON representation of the ActuatorData object.
		"""
		if not data:
			logging.debug("ActuatorData is null. Returning empty string.")
			return ""
		
		logging.debug("Encoding ActuatorData to JSON [pre]  --> " + str(data))
		
		jsonData = self._generateJsonData(obj = data, useDecForFloat = False)
		
		logging.info("Encoding ActuatorData to JSON [post] --> " + str(jsonData))
		return jsonData
	
	def sensorDataToJson(self, data: SensorData = None,useDecForFloat: bool = False):
		"""
		Converts SensorData object to JSON format.
		
		@param data: The SensorData object to be converted.
		@param useDecForFloat: A flag to use Decimal for floating-point numbers in JSON.

		@return: JSON representation of the SensorData object.
		"""
		if not data:
			logging.debug("SensorData is null. Returning empty string.")
			return ""
		
		logging.debug("Encoding SensorData to JSON [pre]  --> " + str(data))
		
		jsonData = self._generateJsonData(obj = data, useDecForFloat = False)
		
		logging.debug("Encoding SensorData to JSON [post] --> " + str(jsonData))
		return jsonData

	def systemPerformanceDataToJson(self, data: SystemPerformanceData = None, useDecForFloat: bool = False):
		"""
		Converts SystemPerformanceData object to JSON format.
		
		@param data: The SystemPerformanceData object to be converted.
		@param useDecForFloat: A flag to use Decimal for floating-point numbers in JSON.

		@return: JSON representation of the SystemPerformanceData object.
		"""
		if not data:
			logging.debug("systemPerformanceData is null. Returning empty string.")
			return ""
		
		logging.debug("Encoding SystemPerformanceData to JSON [pre]  --> " + str(data))
		
		jsonData = self._generateJsonData(obj = data, useDecForFloat = False)
		
		logging.debug("Encoding SystemPerformanceData to JSON [post] --> " + str(jsonData))
		return jsonData
	
	def jsonToActuatorData(self, jsonData: str = None, useDecForFloat: bool = False):
		"""
		Converts JSON string to ActuatorData object.
		
		@param jsonData: The JSON string to be converted.
		@param useDecForFloat: A flag to use Decimal for floating-point numbers in JSON.

		@return: ActuatorData object created from the JSON string.
		"""
		if not jsonData:
			logging.warning("JSON data is empty or null. Returning null.")
			return None
		
		jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat = useDecForFloat)
		
		logging.debug("Converting JSON to ActuatorData [pre]  --> " + str(jsonStruct))
		
		ad = ActuatorData()
		
		self._updateIotData(jsonStruct, ad)
		
		logging.debug("Converted JSON to ActuatorData [post] --> " + str(ad))
		return ad


	def _formatDataAndLoadDictionary(self, jsonData: str, useDecForFloat: bool = False) -> dict:
		"""
		Formats JSON data and loads it into a dictionary.
		
		@param jsonData: The JSON string to be formatted and loaded.
		@param useDecForFloat: A flag to use Decimal for floating-point numbers in JSON.

		@return: A dictionary representing the loaded JSON data.
		"""
		jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		
		jsonStruct = None
		
		if useDecForFloat:
			jsonStruct = json.loads(jsonData, parse_float = Decimal)
		else:
			jsonStruct = json.loads(jsonData)
		
		return jsonStruct
	
	def _generateJsonData(self, obj, useDecForFloat: bool = False) -> str:
		"""
		Generates JSON data from the given object.
		
		@param obj: The object to be converted to JSON.
		@param useDecForFloat: A flag to use Decimal for floating-point numbers in JSON.

		@return: JSON representation of the given object.
		"""
		jsonData = None
		
		if self.encodeToUtf8:
			jsonData = json.dumps(obj, cls = JsonDataEncoder).encode('utf8')
		else:
			jsonData = json.dumps(obj, cls = JsonDataEncoder, indent = 4)
		
		if jsonData:
			jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		
		return jsonData
	
	def _updateIotData(self, jsonStruct, obj):
		"""
		Updates the attributes of the given object using the provided dictionary.
		
		@param jsonStruct: The dictionary containing attribute-value pairs.
		@param obj: The object to be updated based on the dictionary.
		"""
		varStruct = vars(obj)
		
		for key in jsonStruct:
			if key in varStruct:
				setattr(obj, key, jsonStruct[key])
			else:
				logging.warn("JSON data contains key not mappable to object: %s", key)
		
	def jsonToSensorData(self, jsonData: str = None, useDecForFloat: bool = False):
		"""
		Converts JSON string to SensorData object.
		
		@param jsonData: The JSON string to be converted.
		@param useDecForFloat: A flag to use Decimal for floating-point numbers in JSON.

		@return: SensorrData object created from the JSON string.
		"""
		if not jsonData:
			logging.warning("JSON data is empty or null. Returning null.")
			return None
		
		jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat = useDecForFloat)
		
		logging.debug("Converting JSON to SensorData [pre]  --> " + str(jsonStruct))
		
		sd = SensorData()
		
		self._updateIotData(jsonStruct, sd)
		
		logging.debug("Converted JSON to SensorData [post] --> " + str(sd))
		return sd
	
	def jsonToSystemPerformanceData(self, jsonData: str = None, useDecForFloat: bool = False):
		"""
		Converts JSON string to SystemPerformanceData object.
		
		@param jsonData: The JSON string to be converted.
		@param useDecForFloat: A flag to use Decimal for floating-point numbers in JSON.

		@return: SystemPerformanceData object created from the JSON string.
		"""
		if not jsonData:
			logging.warning("JSON data is empty or null. Returning null.")
			return None
		
		jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat = useDecForFloat)
		
		logging.debug("Converting JSON to SystemPerformanceData [pre]  --> " + str(jsonStruct))
		
		sp = SystemPerformanceData()
		
		self._updateIotData(jsonStruct, sp)
		
		logging.debug("Converted JSON to SystemPerformanceData [post] --> " + str(sp))
		return sp
	
class JsonDataEncoder(JSONEncoder):
	"""
	Convenience class to facilitate JSON encoding of an object that
	can be converted to a dict.
	
	"""
	def default(self, o):
		return o.__dict__
	