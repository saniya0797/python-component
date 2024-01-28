#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import psutil
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask


class SystemMemUtilTask(BaseSystemUtilTask):
    """
    Shell representation of class for student implementation.
    Inherits from BaseSystemUtilTask.
    """

    def __init__(self):
        """
        Constructor to initialize the SystemMemUtilTask object.
        """
        super(SystemMemUtilTask, self).__init__(name=ConfigConst.MEM_UTIL_NAME, typeID=ConfigConst.MEM_UTIL_TYPE)

    def getTelemetryValue(self) -> float:
        """
        Retrieves the current memory utilization as telemetry value.

        :return: The memory utilization as a float value.
        """
        return psutil.virtual_memory().percent
