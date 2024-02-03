#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

class HumidifierActuatorSimTask(BaseActuatorSimTask):
	"""
    Represents a simple wrapper for a Humidifier Actuator simulation task.
    Inherits from the BaseActuatorSimTask class.
    """

	def __init__(self):
		"""
        Constructor for HumidifierActuatorSimTask class.
        Initializes the Humidifier actuator simulation task with specific parameters.
        """
		super( \
			HumidifierActuatorSimTask, self).__init__( \
				name = ConfigConst.HUMIDIFIER_ACTUATOR_NAME, \
				typeID = ConfigConst.HUMIDIFIER_ACTUATOR_TYPE, \
				simpleName = "HUMIDIFIER")
		