import logging
import os
import unittest
import redis

import programmingtheiot.common.ConfigConst as ConfigConst

from pathlib import Path
from programmingtheiot.cda.connection.RedisPersistenceAdapter import RedisPersistenceAdapter
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SensorData import SensorData

class RedisPersistenceAdapterTest(unittest.TestCase):

    def setUp(self):
        self.redisAdapter = RedisPersistenceAdapter()
        self.topic = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE

    def tearDown(self):
        self.redisAdapter.disconnectClient()
        self.redisAdapter = None

    def testConnectClient(self):
        # Ensure the client is not connected initially
        self.assertFalse(self.redisAdapter.connectClient())

        # Connect the client
        self.assertTrue(self.redisAdapter.connectClient())

        # Try connecting again - should log a warning and return True
        self.assertTrue(self.redisAdapter.connectClient())

    def testDisconnectClient(self):
        # Ensure the client is not disconnected initially
        self.assertFalse(self.redisAdapter.disconnectClient())

        # Disconnect the client
        self.assertTrue(self.redisAdapter.disconnectClient())

        # Try disconnecting again - should log a warning and return True
        self.assertTrue(self.redisAdapter.disconnectClient())

    def testStoreSensorData(self):
        # Connect the client before storing data
        self.assertTrue(self.redisAdapter.connectClient())

        # Create a sample SensorData
        sensorData = SensorData()
        sensorData.setName("TestSensor")
        sensorData.setValue(25.5)
        sensorData.setSensorType(0)
        sensorData.setStateData("OK")

        # Store the SensorData
        self.assertTrue(self.redisAdapter.storeData(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, sensorData))

        # Disconnect the client after storing data
        self.assertTrue(self.redisAdapter.disconnectClient())

if __name__ == "__main__":
    unittest.main()
