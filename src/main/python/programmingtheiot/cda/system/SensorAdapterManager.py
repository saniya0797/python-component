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

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst
from importlib import import_module
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask

class SensorAdapterManager(object):
	
	def __init__(self):
		"""
        Initializes the SensorAdapterManager object.

        This constructor sets up configuration, initializes the scheduler, and initializes environmental sensor tasks.
        """
		self.configUtil = ConfigUtil()
		self.useEmulator = True
		self.pollRate     = \
			self.configUtil.getInteger( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.POLL_CYCLES_KEY, defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
			
		self.useEmulator  = \
			self.configUtil.getBoolean( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_EMULATOR_KEY)
			
		self.locationID   = \
			self.configUtil.getProperty( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		if self.pollRate <= 0:
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
			
		# technically we only need 1 instance - important to set coalesce
		# to True and allow for misfire grace period
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job( \
			self.handleTelemetry, 'interval', seconds = self.pollRate, max_instances = 2, coalesce = True, misfire_grace_time = 15)
		
		self.dataMsgListener = None
		self.humidityAdapter = None
		self.pressureAdapter = None
		self.tempAdapter     = None

		self._initEnvironmentalSensorTasks()

	def _initEnvironmentalSensorTasks(self):
		"""
        Initializes environmental sensor tasks based on configuration.
        """
		humidityFloor   = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.HUMIDITY_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY)
		humidityCeiling = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.HUMIDITY_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
		
		pressureFloor   = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.PRESSURE_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
		pressureCeiling = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.PRESSURE_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
		
		tempFloor       = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.TEMP_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
		tempCeiling     = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.TEMP_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
		
		if not self.useEmulator:
			self.dataGenerator = SensorDataGenerator()
			
			humidityData = \
				self.dataGenerator.generateDailyEnvironmentHumidityDataSet( \
					minValue = humidityFloor, maxValue = humidityCeiling, useSeconds = False)
			pressureData = \
				self.dataGenerator.generateDailyEnvironmentPressureDataSet( \
					minValue = pressureFloor, maxValue = pressureCeiling, useSeconds = False)
			tempData     = \
				self.dataGenerator.generateDailyIndoorTemperatureDataSet( \
					minValue = tempFloor, maxValue = tempCeiling, useSeconds = False)
			
			self.humidityAdapter = HumiditySensorSimTask(dataSet = humidityData)
			self.pressureAdapter = PressureSensorSimTask(dataSet = pressureData)
			self.tempAdapter     = TemperatureSensorSimTask(dataSet = tempData)

		else:
			heModule = import_module('programmingtheiot.cda.emulated.HumiditySensorEmulatorTask', 'HumiditySensorEmulatorTask')
			heClazz = getattr(heModule, 'HumiditySensorEmulatorTask')
			self.humidityAdapter = heClazz()
			
			peModule = import_module('programmingtheiot.cda.emulated.PressureSensorEmulatorTask', 'PressureSensorEmulatorTask')
			peClazz = getattr(peModule, 'PressureSensorEmulatorTask')
			self.pressureAdapter = peClazz()
			
			teModule = import_module('programmingtheiot.cda.emulated.TemperatureSensorEmulatorTask', 'TemperatureSensorEmulatorTask')
			teClazz = getattr(teModule, 'TemperatureSensorEmulatorTask')
			self.tempAdapter = teClazz()

	def handleTelemetry(self):
		"""
        Handles telemetry data from humidity, pressure, and temperature sensors.
        """
		
		humidityData = self.humidityAdapter.generateTelemetry()
		pressureData = self.pressureAdapter.generateTelemetry()
		tempData     = self.tempAdapter.generateTelemetry()
		
		if humidityData:
			humidityData.setLocationID(self.locationID)
		if pressureData:
			pressureData.setLocationID(self.locationID)
		if tempData:
			tempData.setLocationID(self.locationID)
		
		logging.debug('Generated humidity data: ' + str(humidityData))
		logging.debug('Generated pressure data: ' + str(pressureData))
		logging.debug('Generated temp data: ' + str(tempData))
		
		if self.dataMsgListener:
			if humidityData:
				self.dataMsgListener.handleSensorMessage(humidityData)
			if pressureData:
				self.dataMsgListener.handleSensorMessage(pressureData)
			if tempData:
				self.dataMsgListener.handleSensorMessage(tempData)
		
	def setDataMessageListener(self, listener: IDataMessageListener) :
		if listener:
			self.dataMsgListener = listener
	
	def startManager(self) -> bool:
		logging.info("Started SensorAdapterManager.")
	
		if not self.scheduler.running:
			self.scheduler.start()
			return True
		else:
			logging.info("SensorAdapterManager scheduler already started. Ignoring.")
			return False
		
	def stopManager(self) -> bool:
		logging.info("Stopped SensorAdapterManager.")
	
		try:
			self.scheduler.shutdown()
			return True
		except:
			logging.info("SensorAdapterManager scheduler already stopped. Ignoring.")
			return False