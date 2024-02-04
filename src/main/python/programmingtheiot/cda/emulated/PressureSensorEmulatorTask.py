#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

from programmingtheiot.data.SensorData import SensorData

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask

from pisense import SenseHAT

class PressureSensorEmulatorTask(BaseSensorSimTask):
	
	
	def __init__(self):
		"""
        Initializes the PressureSensorEmulatorTask object.

        This constructor calls the constructor of the parent class (BaseSensorSimTask)
        and sets up the SenseHAT emulator based on the configuration.
        """
		super( \
			PressureSensorEmulatorTask, self).__init__( \
				name = ConfigConst.PRESSURE_SENSOR_NAME, \
				typeID = ConfigConst.PRESSURE_SENSOR_TYPE)
		
		enableEmulation = \
			ConfigUtil().getBoolean( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.sh = SenseHAT(emulate = enableEmulation)
	
	def generateTelemetry(self) -> SensorData:
		"""
        Emulates generating telemetry data for the Pressure Sensor.

        Returns:
            SensorData: The generated SensorData instance representing the telemetry data.
        """
		sensorData = SensorData(name = self.getName() , typeID = self.getTypeID())
		sensorVal = self.sh.environ.pressure
				
		sensorData.setValue(sensorVal)
		self.latestSensorData = sensorData
		
		return sensorData
