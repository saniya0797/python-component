import logging
import redis
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SensorData import SensorData

class RedisPersistenceAdapter(object):

    DATA_GATEWAY_SERVICE = 'Data.GatewayService'

    def __init__(self):
        self.host = None
        self.port = None
        self.redisClient = None

        # Initialize Redis client and connection
        self.initRedisClient()

    def initRedisClient(self):
        try:
            configUtil = ConfigUtil()
            self.host = configUtil.getProperty(self.DATA_GATEWAY_SERVICE, ConfigConst.HOST_KEY, "localhost")
            self.port = configUtil.getInteger(self.DATA_GATEWAY_SERVICE, ConfigConst.PORT_KEY, 6379)

            # Create an instance of the Redis client
            self.redisClient = redis.Redis(host=self.host, port=self.port)
            logging.info("Connected to Redis server at {}:{}".format(self.host, self.port))
        except Exception as e:
            logging.error("Failed to connect to Redis server. Exception: {}".format(str(e)))

    def connectClient(self) -> bool:
        if self.redisClient is not None:
            logging.warning("Redis client is already connected.")
            return True

        try:
            self.initRedisClient()
            return True
        except Exception as e:
            logging.error("Failed to connect to Redis server. Exception: {}".format(str(e)))
            return False

    def disconnectClient(self) -> bool:
        if self.redisClient is None:
            logging.warning("Redis client is already disconnected.")
            return True

        try:
            self.redisClient.close()
            self.redisClient = None
            logging.info("Disconnected from Redis server.")
            return True
        except Exception as e:
            logging.error("Failed to disconnect from Redis server. Exception: {}".format(str(e)))
            return False

    def storeData(self, resource: ResourceNameEnum, data: SensorData) -> bool:
        if self.redisClient is None:
            logging.warning("Redis client is not connected. Cannot store data.")
            return False

        try:
            topic = resource.name
            jsonPayload = data.toJson()
            self.redisClient.publish(topic, jsonPayload)
            logging.info("SensorData published to Redis topic: {}".format(topic))
            return True
        except Exception as e:
            logging.error("Failed to store SensorData in Redis. Exception: {}".format(str(e)))
            return False