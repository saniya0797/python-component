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

class HumiditySensorEmulatorTask(BaseSensorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	from programmingtheiot.data.SensorData import SensorData

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask

from pisense import SenseHAT

class HumiditySensorEmulatorTask(BaseSensorSimTask):

	def __init__(self):
		"""
        Initializes the HumiditySensorEmulatorTask object.

        This constructor calls the constructor of the parent class (BaseSensorSimTask)
        and sets up the SenseHAT emulator based on the configuration.
        """
		super( \
			HumiditySensorEmulatorTask, self).__init__( \
				name = ConfigConst.HUMIDITY_SENSOR_NAME, \
				typeID = ConfigConst.HUMIDITY_SENSOR_TYPE)
		
		enableEmulation = \
			ConfigUtil().getBoolean( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.sh = SenseHAT(emulate = enableEmulation)
	
	def generateTelemetry(self) -> SensorData:
		"""
        Generates telemetry data for the Humidity Sensor.

        Returns:
            SensorData: A SensorData instance containing the generated telemetry data.
        """
		sensorData = SensorData(name = self.getName(), typeID = self.getTypeID())
		sensorVal = self.sh.environ.humidity
				
		sensorData.setValue(sensorVal)
		self.latestSensorData = sensorData
		
		return sensorData