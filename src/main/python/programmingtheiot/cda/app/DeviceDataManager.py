#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
 
import logging
 
from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
 
from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager
 
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ISystemPerformanceDataListener import ISystemPerformanceDataListener
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
 
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
 
class DeviceDataManager(IDataMessageListener):
	"""
	This class manages the overall operation of the device, including sensor data, actuation, and system performance.
	It listens for incoming messages, handles them, and triggers appropriate actions.
	"""
 
	
	def __init__(self):
		"""
		Initializes the DeviceDataManager and sets up various managers and configurations.
		"""
		self.configUtil = ConfigUtil()
		# Enable flags
		self.enableSystemPerf = self.configUtil.getBoolean(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.ENABLE_SYSTEM_PERF_KEY
		)
		self.enableSensing = self.configUtil.getBoolean(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.ENABLE_SENSING_KEY
		)
		self.enableActuation = True  # This can be configured as needed
		# Managers
		self.sysPerfMgr = None
		self.sensorAdapterMgr = None
		self.actuatorAdapterMgr = None
		# Configure managers based on flags
		if self.enableSystemPerf:
			self.sysPerfMgr = SystemPerformanceManager()
			self.sysPerfMgr.setDataMessageListener(self)
			logging.info("Local system performance tracking enabled")
		if self.enableSensing:
			self.sensorAdapterMgr = SensorAdapterManager()
			self.sensorAdapterMgr.setDataMessageListener(self)
			logging.info("Local sensor tracking enabled")
		if self.enableActuation:
			self.actuatorAdapterMgr = ActuatorAdapterManager(dataMsgListener=self)
			logging.info("Local actuation capabilities enabled")
		# Configuration for temperature change handling
		self.handleTempChangeOnDevice = self.configUtil.getBoolean(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY
		)
		self.triggerHvacTempFloor = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY
		)
		self.triggerHvacTempCeiling = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY
		)
 
		pass
	def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
		"""
		Retrieves the named actuator data (response) item from the internal data cache.
		@param name
		@return ActuatorData
		"""
		pass
	def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
		"""
		Retrieves the named sensor data item from the internal data cache.
		@param name
		@return SensorData
		"""
		pass
	def getLatestSystemPerformanceDataFromCache(self, name: str = None) -> SystemPerformanceData:
		"""
		Retrieves the named system performance data from the internal data cache.
		@param name
		@return SystemPerformanceData
		"""
		pass
	def handleActuatorCommandMessage(self, data: ActuatorData) -> bool:
		"""
		This callback method will be invoked by the connection that's handling
		an incoming ActuatorData command message.
		@param data The incoming ActuatorData command message.
		@return boolean
		"""
		logging.info("Actuator data: " + str(data))
		if data:
			logging.info("Processing actuator command message.")
			return self.actuatorAdapterMgr.sendActuatorCommand(data)
		else:
			logging.warning("Incoming actuator command is invalid (null). Ignoring.")
			return False
		pass
	def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
		"""
		This callback method will be invoked by the actuator manager that just
		processed an ActuatorData command, which creates a new ActuatorData
		instance and sets it as a response before calling this method.
		@param data The incoming ActuatorData response message.
		@return boolean
		"""
		if data:
			logging.debug("Incoming actuator response received (from actuator manager): " + str(data))
			# Store the data in the cache
			self.actuatorResponseCache[data.getName()] = data
			# Convert ActuatorData to JSON and get the msg resource
			actuatorMsg = DataUtil().actuatorDataToJson(data)
			resourceEnum = ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE
			# Delegate to the transmit function any potential upstream comm's
			self._handleUpstreamTransmission(resourceEnum, actuatorMsg)
			return True
		else:
			logging.warning("Incoming actuator response is invalid (null). Ignoring.")
			return False
		pass
	def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
		"""
		This callback method is generic and designed to handle any incoming string-based
		message, which will likely be JSON-formatted and need to be converted to the appropriate
		data type. You may not need to use this callback at all.
		@param data The incoming JSON message.
		@return boolean
		"""
		logging.info("Handling incoming message from resource " + str(resourceEnum))
		self._handleIncomingDataAnalysis(msg)  # Implement this as needed
		return True
		pass
	def handleSensorMessage(self, data: SensorData) -> bool:
		"""
		This callback method will be invoked by the sensor manager that just processed
		a new sensor reading, which creates a new SensorData instance that will be
		passed to this method.
		@param data The incoming SensorData message.
		@return boolean
		"""
		if data:
			logging.debug("Incoming sensor data received (from sensor manager): " + str(data))
			self._handleSensorDataAnalysis(data)
			return True
		else:
			logging.warning("Incoming sensor data is invalid (null). Ignoring.")
			return False
		pass
	def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
		"""
		This callback method will be invoked by the system performance manager that just
		processed a new sensor reading, which creates a new SystemPerformanceData instance
		that will be passed to this method.
		@param data The incoming SystemPerformanceData message.
		@return boolean
		"""
		if data:
			logging.debug("Incoming system performance message received (from sys perf manager): " + str(data))
			# Implement handling of system performance data here as needed
			return True
		else:
			logging.warning("Incoming system performance data is invalid (null). Ignoring.")
			return False		
		pass
	def setSystemPerformanceDataListener(self, listener: ISystemPerformanceDataListener = None):
		pass
	def setTelemetryDataListener(self, name: str = None, listener: ITelemetryDataListener = None):
		pass
	def startManager(self):
		logging.info("Starting DeviceDataManager...")
		if self.sysPerfMgr:
			self.sysPerfMgr.startManager()
		if self.sensorAdapterMgr:
			self.sensorAdapterMgr.startManager()
		logging.info("Started DeviceDataManager.")
		pass
	def stopManager(self):
		logging.info("Stopping DeviceDataManager...")
		if self.sysPerfMgr:
			self.sysPerfMgr.stopManager()
		if self.sensorAdapterMgr:
			self.sensorAdapterMgr.stopManager()
		logging.info("Stopped DeviceDataManager.")	
		pass
	def _handleIncomingDataAnalysis(self, msg: str):
		"""
		Call this from handleIncomeMessage() to determine if there's
		any action to take on the message. Steps to take:
		1) Validate msg: Most will be ActuatorData, but you may pass other info as well.
		2) Convert msg: Use DataUtil to convert if appropriate.
		3) Act on msg: Determine what - if any - action is required, and execute.
		"""
		pass
	def _handleSensorDataAnalysis(self, data: SensorData):
		"""
		Call this from handleSensorMessage() to determine if there's
		any action to take on the message. Steps to take:
		1) Check config: Is there a rule or flag that requires immediate processing of data?
		2) Act on data: If # 1 is true, determine what - if any - action is required, and execute.
		"""
 
		logging.info("Handling sensor data: " + str(data))
		if self.handleTempChangeOnDevice and data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
			ad = ActuatorData(typeID=ConfigConst.HVAC_ACTUATOR_TYPE)
			if data.getValue() > self.triggerHvacTempCeiling:
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacTempCeiling)
			elif data.getValue() < self.triggerHvacTempFloor:
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacTempFloor)
			else:
				ad.setCommand(ConfigConst.COMMAND_OFF)
			# Send actuator command to manager
			self.handleActuatorCommandMessage(ad)
		pass
	def _handleUpstreamTransmission(self, resourceName: ResourceNameEnum, msg: str):
		"""
		Call this from handleActuatorCommandResponse(), handlesensorMessage(), and handleSystemPerformanceMessage()
		to determine if the message should be sent upstream. Steps to take:
		1) Check connection: Is there a client connection configured (and valid) to a remote MQTT or CoAP server?
		2) Act on msg: If # 1 is true, send message upstream using one (or both) client connections.
		"""
		pass