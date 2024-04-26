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
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ISystemPerformanceDataListener import ISystemPerformanceDataListener
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.cda.connection.CoapServerAdapter import CoapServerAdapter
#from programmingtheiot.connection.RedisPersistenceAdapter import RedisPersistenceAdapter
 

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.common.ConfigUtil import ConfigUtil
class DeviceDataManager(IDataMessageListener):
	"""
	Shell representation of class for student implementation.
	"""
	def __init__(self):
		self.configUtil = ConfigUtil()
		self.enableSystemPerf   = \
			self.configUtil.getBoolean( \
									section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_SYSTEM_PERF_KEY)
		self.enableSensing      = \
			self.configUtil.getBoolean( \
									section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_SENSING_KEY)
		self.enableCoapServer = \
			self.configUtil.getBoolean( \
									section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_COAP_SERVER_KEY)
		# NOTE: this can also be retrieved from the configuration file
		self.enableActuation    = True
		self.sysPerfMgr         = None
		self.sensorAdapterMgr   = None
		self.actuatorAdapterMgr = None
		# NOTE: The following aren't used until Part III but should be declared now
		self.mqttClient         = None
		self.coapClient         = None
		self.coapServer         = None
		# instantiating SystemPerformanceManager and setting the IDataMessageListener.
		if self.enableSystemPerf:
			self.sysPerfMgr = SystemPerformanceManager()
			self.sysPerfMgr.setDataMessageListener(self)
			logging.info("Local system performance tracking enabled")

		# instantiating SensorAdapterManager and setting the IDataMessageListener.
		if self.enableSensing:
			self.sensorAdapterMgr = SensorAdapterManager()
			self.sensorAdapterMgr.setDataMessageListener(self)
			logging.info("Local sensor tracking enabled")
			
		# instantiating ActuatorAdapterManager and setting the IDataMessageListener.
		if self.enableActuation:
			self.actuatorAdapterMgr = ActuatorAdapterManager(dataMsgListener = self)
			logging.info("Local actuation capabilities enabled")
		# Retrieving the actuation enabling boolean flags from the configuration file
		self.handleTempChangeOnDevice = \
			self.configUtil.getBoolean( \
									ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
		self.triggerHvacTempFloor     = \
			self.configUtil.getFloat( \
									ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY);
		self.triggerHvacTempCeiling   = \
			self.configUtil.getFloat( \
									ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY);
		self.handlePressureChangeOnDevice = \
			self.configUtil.getBoolean( \
									ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HANDLE_PRESSURE_CHANGE_ON_DEVICE_KEY)
		self.triggerHvacPressureFloor     = \
			self.configUtil.getFloat( \
									ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_PRESSURE_FLOOR_KEY);
		self.triggerHvacPressureCeiling   = \
			self.configUtil.getFloat( \
									ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_PRESSURE_CEILING_KEY);
		self.enableMqttClient = \
			self.configUtil.getBoolean( \
								section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_MQTT_CLIENT_KEY)
		self.mqttClient = None
		if self.enableMqttClient:
			self.mqttClient = MqttClientConnector("test1")
			self.mqttClient.setDataMessageListener(self)
		if self.enableCoapServer:
			self.coapServer = CoapServerAdapter(dataMsgListener = self)
		self.enableCoapClient = \
		self.configUtil.getBoolean( \
			section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_COAP_CLIENT_KEY)
		if self.enableCoapClient :
			self.coapClient = CoapClientConnector(dataMsgListener = self)
		# Create a class-scoped instance of RedisPersistenceAdapter
		#self.redisClient = RedisPersistenceAdapter()
		#self.enableRedisStorage = False  # boolean flag to enable/disable storage to Redis
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
			return None

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
			# store the data in the cache
			self.actuatorResponseCache[data.getName()] = data
			# convert ActuatorData to JSON and get the msg resource
			actuatorMsg = DataUtil().actuatorDataToJson(data)
			resourceName = ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE
			# delegate to the transmit function any potential upstream comm's
			self._handleUpstreamTransmission(resource = resourceName, msg = actuatorMsg)
			return True
		else:
			logging.warning("Incoming actuator response is invalid (null). Ignoring.")
			return False
	def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
		"""
		This callback method is generic and designed to handle any incoming string-based
		message, which will likely be JSON-formatted and need to be converted to the appropriate
		data type. You may not need to use this callback at all.
		@param data The incoming JSON message.
		@return boolean
		"""
		logging.info("Incoming: " + ResourceNameEnum(resourceEnum) + "Message: " + str(msg))
	def handleSensorMessage(self, data: SensorData) -> bool:
		"""
		This callback method will be invoked by the sensor manager that just processed
		a new sensor reading, which creates a new SensorData instance that will be
		passed to this method.
		@param data The incoming SensorData message.
		@return boolean
		"""
		if data:
			logging.info("Incoming sensor data received (from sensor manager): " + str(data))
			# TODO: Optionally, implement `_handleSensorDataAnalysis()` to handle internal analytics
			self._handleSensorDataAnalysis(data)
			# Convert the `SensorData` instance to JSON
			jsonData = DataUtil().sensorDataToJson(data = data)
			# Pass the resource and newly generated JSON data to `_handleUpstreamTransmission()`
			self._handleUpstreamTransmission(resourceName = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg = jsonData)
			return True
		else:
			logging.warning("Incoming sensor data is invalid (null). Ignoring.")
			return False
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
			return True
		else:
			logging.warning("Incoming system performance data is invalid (null). Ignoring.")
			return False
	def setSystemPerformanceDataListener(self, listener: ISystemPerformanceDataListener = None):
		pass
	def setTelemetryDataListener(self, name: str = None, listener: ITelemetryDataListener = None):
		pass
	def startManager(self):
		"""
		Checks for the SystemPerformanceManager and SensorAdapterManager status and starts them.
		"""
		logging.info("Starting DeviceDataManager...")
		if self.sysPerfMgr:
			self.sysPerfMgr.startManager()
		if self.sensorAdapterMgr:
			self.sensorAdapterMgr.startManager()
		if self.mqttClient:
			self.mqttClient.connectClient()
			self.mqttClient.subscribeToTopic(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, callback = None, qos = ConfigConst.DEFAULT_QOS)
		if self.coapServer:
			self.coapServer.startServer()
		logging.info("Started DeviceDataManager.")
	def stopManager(self):
		"""
		Checks for the SystemPerformanceManager and SensorAdapterManager status and stops them.
		"""
		logging.info("Stopping DeviceDataManager...")
		if self.sysPerfMgr:
			self.sysPerfMgr.stopManager()
		if self.sensorAdapterMgr:	
			self.sensorAdapterMgr.stopManager()
		if self.mqttClient:
			self.mqttClient.unsubscribeFromTopic(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE)
			self.mqttClient.disconnectClient()
		if self.coapServer:
			self.coapServer.stopServer()
		logging.info("Stopped DeviceDataManager.")
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
		if self.handleTempChangeOnDevice and data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
			logging.info("Handle temp change: %s - type ID: %s", str(self.handleTempChangeOnDevice), str(data.getTypeID()))
			ad = ActuatorData(typeID = ConfigConst.HVAC_ACTUATOR_TYPE)
			if data.getValue() > self.triggerHvacTempCeiling:
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacTempCeiling)
			elif data.getValue() < self.triggerHvacTempFloor:
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacTempFloor)
			else:
				ad.setCommand(ConfigConst.COMMAND_OFF)
			self.handleActuatorCommandMessage(ad)
		"""if self.handlePressureChangeOnDevice and data.getTypeID() == ConfigConst.PRESSURE_SENSOR_TYPE:
			logging.info("Handle pressure change: %s - type ID: %s", str(self.handlePressureChangeOnDevice), str(data.getTypeID()))
			ad = ActuatorData(typeID = ConfigConst.HVAC_ACTUATOR_TYPE)
			if data.getValue() > self.triggerHvacPressureCeiling:
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacPressureCeiling)
			elif data.getValue() < self.triggerHvacPressureFloor:
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacPressureFloor)
			else:
				ad.setCommand(ConfigConst.COMMAND_OFF)
			# NOTE: ActuatorAdapterManager and its associated actuator
			# task implementations contain logic to avoid processing
			# duplicative actuator commands - for the purposes
			# of this exercise, the logic for filtering commands is
			# left to ActuatorAdapterManager and its associated actuator
			# task implementations, and not this function
			self.handleActuatorCommandMessage(ad)"""
	def _handleUpstreamTransmission(self, resourceName: ResourceNameEnum, msg: str):
		"""
		Call this from handleActuatorCommandResponse(), handlesensorMessage(), and handleSystemPerformanceMessage()
		to determine if the message should be sent upstream. Steps to take:
		1) Check connection: Is there a client connection configured (and valid) to a remote MQTT or CoAP server?
		2) Act on msg: If # 1 is true, send message upstream using one (or both) client connections.
		"""
		logging.info("Upstream transmission invoked. Checking comm's integration.")
		# NOTE: If using MQTT, the following will attempt to publish the message to the broker
		if self.mqttClient:
			if self.mqttClient.publishMessage(resource = resourceName, msg = msg):
				logging.debug("Published incoming data to resource (MQTT): %s", str(resourceName))
			else:
				logging.warning("Failed to publish incoming data to resource (MQTT): %s", str(resourceName))
		# NOTE: If using CoAP, the following will attempt to PUT the message to the server
		if self.coapClient:
			if self.coapClient.sendPutRequest(resource = resourceName, payload = msg):
				logging.debug("Put incoming message data to resource (CoAP): %s", str(resourceName))
			else:
				logging.warning("Failed to put incoming message data to resource (CoAP): %s", str(resourceName))
