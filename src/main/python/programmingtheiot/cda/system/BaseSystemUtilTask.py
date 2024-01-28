#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import programmingtheiot.common.ConfigConst as ConfigConst


class BaseSystemUtilTask:
    """
    Shell implementation representation of class for student implementation.
    """

    def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE):
        """
        Constructor to initialize the BaseSystemUtilTask object.

        :param name: The name of the system utilization task.
        :param typeID: The type ID of the system utilization task.
        """
        self.name = name
        self.typeID = typeID

    def getName(self) -> str:
        """
        Gets the name of the system utilization task.

        :return: The name of the task.
        """
        return self.name

    def getTypeID(self) -> int:
        """
        Gets the type ID of the system utilization task.

        :return: The type ID of the task.
        """
        return self.typeID

    def getTelemetryValue(self) -> float:
        """
        Template method definition. Sub-class will implement this to retrieve
        the system utilization measure.

        :return: The telemetry value as a float.
        """
        pass
