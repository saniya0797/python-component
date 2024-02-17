#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask

from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from apscheduler.schedulers.background import BackgroundScheduler


class SystemPerformanceManager(object):
    """
    Shell representation of class for student implementation.
    Manages system performance tasks, such as CPU and memory utilization.
    """

    def __init__(self):
        """
        Constructor to initialize the SystemPerformanceManager object.
        """
        # Create an instance of ConfigUtil for configuration
        configUtil = ConfigUtil()

        # Retrieve poll rate from configuration
        self.pollRate = configUtil.getInteger(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.POLL_CYCLES_KEY,
            defaultVal=ConfigConst.DEFAULT_POLL_CYCLES)

        # Retrieve location ID from configuration
        self.locationID = configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.DEVICE_LOCATION_ID_KEY,
            defaultVal=ConfigConst.NOT_SET)

        # Set default poll rate if the retrieved value is invalid
        if self.pollRate <= 0:
            self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES

        # Initialize data message listener to None
        self.dataMsgListener = None

        # Initialize the scheduler for background jobs
        self.scheduler = BackgroundScheduler()
        # Schedule the handleTelemetry method to run at a fixed interval
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate)

        # Create instances of system utilization tasks
        self.cpuUtilTask = SystemCpuUtilTask()
        self.memUtilTask = SystemMemUtilTask()

    def handleTelemetry(self):
        """
        Handles telemetry by retrieving and logging CPU and memory utilization.
        """
        cpuUtilPct = self.cpuUtilTask.getTelemetryValue()
        memUtilPct = self.memUtilTask.getTelemetryValue()
        # Retrieve CPU and memory utilization values
        self.cpuUtilPct = self.cpuUtilTask.getTelemetryValue()
        self.memUtilPct = self.memUtilTask.getTelemetryValue()
        
        logging.debug('CPU utilization is %s percent, and memory utilization is %s percent.', str(cpuUtilPct), str(memUtilPct))
        
        sysPerfData = SystemPerformanceData()
        sysPerfData.setLocationID(self.locationID)
        sysPerfData.setCpuUtilization(self.cpuUtilPct)
        sysPerfData.setMemoryUtilization(self.memUtilPct)
        
        if self.dataMsgListener:
            self.dataMsgListener.handleSystemPerformanceMessage(data = sysPerfData)

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener:
            self.dataMsgListener = listener


    def startManager(self):
        """
        Starts the SystemPerformanceManager if it is not already started.
        """
        logging.info("Starting SystemPerformanceManager...")

        # Check if the scheduler is not running, then start it
        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("Started SystemPerformanceManager.")
        else:
            logging.warning("SystemPerformanceManager scheduler already started. Ignoring.")

    def stopManager(self):
        """
        Stops the SystemPerformanceManager and shuts down the scheduler.
        """
        logging.info("Stopping SystemPerformanceManager...")

        try:
            # Shutdown the scheduler
            self.scheduler.shutdown()
            logging.info("Stopped SystemPerformanceManager.")
        except:
            logging.warning("SystemPerformanceManager scheduler already stopped. Ignoring.")
