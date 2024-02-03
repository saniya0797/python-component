#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import random

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataSet

class BaseSensorSimTask():
	
	DEFAULT_MIN_VAL = ConfigConst.DEFAULT_VAL
	DEFAULT_MAX_VAL = 100.0

	
	
	def __init__(self, name = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, dataSet = None, minVal: float = DEFAULT_MIN_VAL, maxVal: float = DEFAULT_MAX_VAL):
		"""
        Constructor for BaseSensorSimTask class.
        
        @param name The name of the sensor task.
        @param typeID The type ID of the sensor task.
        @param dataSet The data set for simulation (optional).
        @param minVal The minimum value for simulation (used when dataSet is not provided).
        @param maxVal The maximum value for simulation (used when dataSet is not provided).
        """
		self.dataSet = dataSet
		self.name = name
		self.typeID = typeID
		self.dataSetIndex = 0
		self.useRandomizer = False
		
		self.latestSensorData = None
		
		if not self.dataSet:
			self.useRandomizer = True
			self.minVal = minVal
			self.maxVal = maxVal
	
	def generateTelemetry(self) -> SensorData:
		"""
        Generates telemetry data for the sensor task.
        Sensor-specific functionality should be implemented by a sub-class.
        
        @return SensorData The generated sensor data.
        """
		sensorData = SensorData(typeID = self.getTypeID(), name = self.getName())
		sensorVal = ConfigConst.DEFAULT_VAL
		
		if self.useRandomizer:
			sensorVal = random.uniform(self.minVal, self.maxVal)
		else:
			sensorVal = self.dataSet.getDataEntry(index = self.dataSetIndex)
			self.dataSetIndex = self.dataSetIndex + 1
			
			if self.dataSetIndex >= self.dataSet.getDataEntryCount() - 1:
				self.dataSetIndex = 0
				
		sensorData.setValue(sensorVal)
		
		self.latestSensorData = sensorData
		
		return self.latestSensorData
	
	def getTelemetryValue(self) -> float:
		"""
        Gets the telemetry value from the latest sensor data.
        If the sensor data hasn't been created, calls self.generateTelemetry() first.
        
        @return float The current telemetry value.
        """
		if not self.latestSensorData:
			self.generateTelemetry()
		
		return self.latestSensorData.getValue()
	
	def getLatestTelemetry(self) -> SensorData:
		"""
        Gets the current SensorData instance or a copy.
        
        @return SensorData The current sensor data.
        """
		pass
	
	def getName(self) -> str:
		"""
        Gets the name of the sensor task.
        
        @return str The name of the sensor task.
        """
		return self.name
	
	def getTypeID(self) -> int:
		"""
        Gets the type ID of the sensor task.
        
        @return int The type ID of the sensor task.
        """
		return self.typeID
	