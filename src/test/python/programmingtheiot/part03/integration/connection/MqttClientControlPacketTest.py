import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData 
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData 
from programmingtheiot.data.DataUtil import DataUtil

class MqttClientControlPacketTest(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Executing the MqttClientControlPacketTest class...")
		
		self.cfg = ConfigUtil()
		
		# NOTE: Be sure to use a DIFFERENT clientID than that which is used
		# for your CDA when running separately from this test
		# 
		# The clientID shown below is an example only - please use your own
		# unique value for this test
		client_id = "MyTestMqttClient001"
		self.mcc = MqttClientConnector(clientID = client_id )
		pass
		
	def setUp(self):
		
		pass

	def tearDown(self):
		pass

	def testConnectAndDisconnect(self):
		# TODO: implement this test
		self.mcc.connectClient()
		# self.mcc.connect()
		sleep(30)  # Allow time for the connection to be established
		self.assertTrue(self.mcc.mqttClient.is_connected())
		self.mcc.disconnectClient()
		sleep(30)  # Allow time for the disconnection
		self.assertFalse(self.mcc.mqttClient.is_connected())
		pass
	
	def testServerPing(self):
		# TODO: implement this test
		self.assertTrue(self.mcc.connectClient())
		sleep(3)
		self.assertTrue(self.mcc.publishMessage(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg="Hello, MQTT!", qos=1))

		sleep(20)
        
		pass
	
	def testPubSub(self):
		# TODO: implement this test
		# 
		# IMPORTANT: be sure to use QoS 1 and 2 to see ALL control packets
		self.assertTrue(self.mcc.connectClient())
    	 # Wait for connection to establish
		sleep(20) 

        # Subscribe to a topic
		self.assertTrue(self.mcc.subscribeToTopic(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, qos=1))


        # Publish a message
		self.assertTrue(self.mcc.publishMessage(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg="Hello, MQTT!", qos=1))


        # Wait for the message to be received
		sleep(200)


        # Unsubscribe from the topic
		self.assertTrue(self.mcc.unsubscribeFromTopic(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE))
		self.assertTrue(self.mcc.disconnectClient())

	def testPubSubb(self):
		# TODO: implement this test
		# 
		# IMPORTANT: be sure to use QoS 1 and 2 to see ALL control packets
		self.assertTrue(self.mcc.connectClient())
    	 # Wait for connection to establish
		sleep(2) 

        # Subscribe to a topic
		self.assertTrue(self.mcc.subscribeToTopic(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, qos=2))


        # Publish a message
		self.assertTrue(self.mcc.publishMessage(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg="Hello, MQTT!", qos=2))


        # Wait for the message to be received
		sleep(200)


        # Unsubscribe from the topic
		self.assertTrue(self.mcc.unsubscribeFromTopic(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE))
		self.assertTrue(self.mcc.disconnectClient())




        
		pass	
if __name__ == "__main__":
	unittest.main()
	

    