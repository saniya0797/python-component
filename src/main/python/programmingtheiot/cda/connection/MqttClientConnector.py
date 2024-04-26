#####
#
# This class is part of the Programming the Internet of Things project.
#
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import logging
import paho.mqtt.client as mqttClient
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient
from programmingtheiot.data.DataUtil import DataUtil
 
import ssl
 
class MqttClientConnector(IPubSubClient):
    """
    This class implements the IPubSubClient interface to provide MQTT connectivity.
    It handles connecting, disconnecting, publishing, and subscribing to topics
    on an MQTT broker.
    """
    def __init__(self, clientID: str = None):
        """
        Initializes the MQTT client with configuration settings.
        The client ID can be passed, or it will be generated based on configuration.
        It sets up the MQTT broker information and client connection based on the configuration.
        """
        # Configuration and initialization of MQTT client
        self.config = ConfigUtil()
        self.dataMsgListener = None
        self.host = \
            self.config.getProperty( \
                ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
        self.port = \
            self.config.getInteger( \
                                ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_MQTT_PORT)
        self.keepAlive = \
            self.config.getInteger( \
                                ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
        self.defaultQos = \
            self.config.getInteger( \
                                ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.DEFAULT_QOS_KEY, ConfigConst.DEFAULT_QOS)
        self.enableEncryption = \
            self.config.getBoolean( \
                                    ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.ENABLE_CRYPT_KEY)
 
        self.pemFileName = \
            self.config.getProperty( \
                                     ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.CERT_FILE_KEY)
        self.mqttClient = None
        self.clientID = None
        self.buf = None
        self.pingSent = False
        self.pingReceived = False
        # IMPORTANT:
        #
        # You can choose to set clientID in a number of ways:
        #  1 - use the locationID value in PiotConfig.props as the clientID (see below)
        #  2 - pass a custom clientID into constructor (from DeviceDataManager or your test)
        #  3 - hard code a clientID in this constructor (generally not recommended)
        #  4 - if using Python Paho, set NO client ID and let broker auto-assign
        #      a random value (not recommended if setting clean session flag to False)
        # TODO: the following is just a sample; use your own unique ID
        if not self.clientID:
            self.clientID = \
                self.config.getProperty( \
                                        ConfigConst.CONSTRAINED_DEVICE, ConfigConst.DEVICE_LOCATION_ID_KEY)
        # TODO: be sure to validate the clientID!
        logging.info('\tMQTT Client ID:   ' + self.clientID)
        logging.info('\tMQTT Broker Host: ' + self.host)
        logging.info('\tMQTT Broker Port: ' + str(self.port))
        logging.info('\tMQTT Keep Alive:  ' + str(self.keepAlive))
    def connectClient(self) -> bool:
        """
        Connects to the MQTT broker using the configured settings.
        If already connected, it ignores the request.
        """
        # Connection logic
        self.caCertFile = self.config.getProperty(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.CERT_FILE_KEY)
        if not self.mqttClient:
            # TODO: make clean_session configurable
            self.mqttClient = mqttClient.Client(client_id = self.clientID, clean_session = True)
            try:
                if self.enableEncryption:
                    logging.info("Enabling TLS encryption...")
                    self.port = \
                        self.config.getInteger( \
                            ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.SECURE_PORT_KEY, ConfigConst.DEFAULT_MQTT_SECURE_PORT)
                    self.mqttClient.tls_set(self.caCertFile, tls_version = ssl.PROTOCOL_TLSv1_2)
            except:
                logging.warning("Failed to enable TLS encryption. Using unencrypted connection.")
            self.mqttClient.on_connect = self.onConnect
            self.mqttClient.on_disconnect = self.onDisconnect
            self.mqttClient.on_message = self.onMessage
            self.mqttClient.on_publish = self.onPublish
            self.mqttClient.on_subscribe = self.onSubscribe
        if not self.mqttClient.is_connected():
            logging.info('MQTT client connecting to broker at host: ' + self.host)
            self.mqttClient.connect(self.host, self.port, self.keepAlive)
            self.mqttClient.loop_start()
            return True
        else:
            logging.warning('MQTT client is already connected. Ignoring connect request.')
            return False
    # Implementing MQTT client disconnect method
    def disconnectClient(self) -> bool:
        """
        Disconnects from the MQTT broker.
        If already disconnected, it ignores the request.
        """
        if self.mqttClient.is_connected():
            logging.info('Disconnecting MQTT client from broker: ' + self.host)
            self.mqttClient.loop_stop()
            self.mqttClient.disconnect()
            return True
        else:
            logging.warning('MQTT client already disconnected. Ignoring.')
            return False

    def onConnect(self, client, userdata, flags, rc):
        """
        Callback method triggered when the MQTT client connects to the broker.
        """
        logging.info('MQTT client connected to broker: ' + str(client))
        logging.info('[Callback] Connected to MQTT broker. Result code: ' + str(rc))
        # NOTE: Be sure to set `self.defaultQos` during instantiation!
        self.mqttClient.subscribe( \
            topic = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value, qos = self.defaultQos)
        self.mqttClient.message_callback_add( \
            sub = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value, \
            callback = self.onActuatorCommandMessage)
    def onDisconnect(self, client, userdata, rc):
        """
        Callback method triggered when the MQTT client disconnects from the broker.
        """
        logging.info('MQTT client disconnected from broker: ' + str(client))
    def onMessage(self, client, userdata, msg):
        """
        Callback method triggered when an MQTT message is received.
        """
        payload = msg.payload
        if payload:
            logging.info('MQTT message received with payload: ' + str(payload.decode("utf-8")))
            return True
        else:
            logging.info('MQTT message received with no payload: ' + str(msg))
            return False

    def onPublish(self, client, userdata, mid):
        """
        Callback method triggered when an MQTT message is published.
        """
        logging.info('MQTT message published: ' + str(client))
    def onSubscribe(self, client, userdata, mid, granted_qos):
        logging.info('MQTT client subscribed: ' + str(client))
    def onPing(self,client, userdata, level, buf):
        """
        This is a callback that is called once a new MQTT log message is published. In this case,
        it looks for a PINGREQ and a PINGRESP in the logs and sets a @self.pingSent and @self.pingResponse
        variables to True
        @param client The client reference context.
        @param userdata The user reference context.
        @param level The debug level to filter
        @param buf The buffer in which the debug messages will be stored
        """
        self.buf = buf
        request = 'PINGREQ'
        response = 'PINGRESP'
        if (request in buf):
            self.pingSent = True
        elif (response in buf):
            self.pingReceived = True    
    def onActuatorCommandMessage(self, client, userdata, msg):
        """
        This callback is defined as a convenience, but does not
        need to be used and can be ignored.
        It's simply an example for how you can create your own
        custom callback for incoming messages from a specific
        topic subscription (such as for actuator commands).
        @param client The client reference context.
        @param userdata The user reference context.
        @param msg The message context, including the embedded payload.
        """
        logging.info('[Callback] Actuator command message received. Topic: %s.', msg.topic)
        if self.dataMsgListener:
            try:
                # assumes all data is encoded using UTF-8 (between GDA and CDA)
                actuatorData = DataUtil().jsonToActuatorData(msg.payload.decode('utf-8'))
                self.dataMsgListener.handleActuatorCommandMessage(actuatorData)
            except:
                logging.exception("Failed to convert incoming actuation command payload to ActuatorData: ")
    def publishMessage(self, resource: ResourceNameEnum = None, msg: str = None, qos: int = ConfigConst.DEFAULT_QOS):
        """
        Publishes a message to a specified topic with a given QoS.
        Validates the topic and message before publishing.
        """

        # check validity of resource (topic)
        if not resource:
            logging.warning('No topic specified. Cannot publish message.')
            return False
        # check validity of message
        if not msg:
            logging.warning('No message specified. Cannot publish message to topic: ' + resource.value)
            return False
        # check validity of QoS - set to default if necessary
        if qos < 0 or qos > 2:
            qos = ConfigConst.DEFAULT_QOS
        # publish message, and wait for publish to complete before returning
        msgInfo = self.mqttClient.publish(topic = resource.value, payload = msg, qos = qos)
        msgInfo.wait_for_publish()
        return True

    def subscribeToTopic(self, resource: ResourceNameEnum = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS):
        """
        Subscribes to a specified topic with a given QoS.
        Validates the topic before subscribing.
        """

        # check validity of resource (topic)
        if not resource:
            logging.warning('No topic specified. Cannot subscribe.')
            return False
        # check validity of QoS - set to default if necessary
        if qos < 0 or qos > 2:
            qos = ConfigConst.DEFAULT_QOS
        # subscribe to topic
        logging.info('Subscribing to topic %s', resource.value)
        self.mqttClient.subscribe(resource.value, qos)
        return True

    def unsubscribeFromTopic(self, resource: ResourceNameEnum = None):
        """
        Unsubscribes from a specified topic.
        Validates the topic before unsubscribing.
        """
        # check validity of resource (topic)
        if not resource:
            logging.warning('No topic specified. Cannot unsubscribe.')
            return False
        logging.info('Unsubscribing to topic %s', resource.value)
        self.mqttClient.unsubscribe(resource.value)
        return True
    def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
        """
        Sets a data message listener for handling incoming messages.
        """
        if listener:
            self.dataMsgListener = listener