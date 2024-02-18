import unittest
from programmingtheiot.cda.connection.RedisPersistenceAdapter import RedisPersistenceAdapter
import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil

from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SensorData import SensorData
from time import sleep

class RedisPersistenceAdapterTest(unittest.TestCase):
    def setUp(self):
        self.redisClient = RedisPersistenceAdapter()

    def tearDown(self):
        self.redisClient.disconnectClient()

    def testConnectClient(self):
        self.assertTrue(self.redisClient.connectClient())
        # Additional assertions or checks if needed

    def testDisconnectClient(self):
        # Ensure the client is connected before attempting to disconnect
        self.assertTrue(self.redisClient.connectClient())
        self.assertTrue(self.redisClient.disconnectClient())
        # Additional assertions or checks if needed

    def testStoreSensorData(self):
        self.assertTrue(self.redisClient.connectClient())

        # Create a sample SensorData object
        sensor_data = SensorData()
        sensor_data.setName(ResourceNameEnum.HUMIDITY)
        sensor_data.setValue(50.0)
        sensor_data.setSensorType(ResourceNameEnum.HUMIDITY_SENSOR)

        # Store the SensorData in Redis
        self.assertTrue(self.redisClient.storeData(ResourceNameEnum.HUMIDITY_SENSOR, sensor_data))

        # Sleep for a short duration to allow Redis to process the data
        sleep(1)

        # Additional assertions or checks if needed

if __name__ == '__main__':
    unittest.main()
