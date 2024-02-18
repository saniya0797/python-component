import logging
import socket
import redis
import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil

from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SensorData import SensorData

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.cda.connection.IRequestResponseClient import IRequestResponseClient


class RedisPersistenceAdapter:
    
    DATA_GATEWAY_SERVICE = 'Data.GatewayService'
	
    
    def __init__(self):
        """
		Constructor for RedisPersistenceAdapter.
		Initializes class variables and sets up the logger, configuration, and Redis client.
		"""
        
        self.host = None
        self.port = None
        self.redis_client = None
        self.connected = False

        # Initialize logging (adjust as needed)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Retrieve host and port from the configuration file
        self.load_config()
         # Create an instance of the Redis client using host and port
        
        self.create_redis_client()

    def load_config(self):
        """
        Loads configuration settings from the ConfigUtil for Redis connection.
        """
        try:
            config_util = ConfigUtil()
            config = config_util.get_config(ConfigConst.DATA_GATEWAY_SERVICE)
            self.host = config['host']
            self.port = int(config['port'])
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")

    def create_redis_client(self):
        """
        Creates an instance of the Redis client using the configured host and port.
        """
        try:
            self.redis_client = Redis(host=self.host, port=self.port)
            self.logger.info("Redis client created.")
        except Exception as e:
            self.logger.error(f"Error creating Redis client: {e}")

    def connectClient(self) -> bool:
        """
        Connects to the Redis server. Returns True if successful, False otherwise.
        """
        if self.connected:
            self.logger.warning("Redis client is already connected.")
            return True

        try:
            self.redis_client = Redis(host=self.host, port=self.port)
            self.connected = True
            self.logger.info("Connected to Redis.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to Redis: {e}")
            return False

    def disconnectClient(self) -> bool:
        """
        Disconnects from the Redis server. Returns True if successful, False otherwise.
        """
        if not self.connected:
            self.logger.warning("Redis client is already disconnected.")
            return True

        try:
            self.redis_client.close()
            self.connected = False
            self.logger.info("Disconnected from Redis.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to disconnect from Redis: {e}")
            return False

    def storeData(self, resource: ResourceNameEnum, data: SensorData) -> bool:
        """
        Stores SensorData in Redis with a key based on the resource and timestamp.
        Returns True if successful, False otherwise.
        """
        try:
            # Construct your Redis key based on the chosen pattern
            key = f"{resource.value}:{data.timestamp}"  # Adjust as needed
            # Convert data to a format suitable for storage in Redis (e.g., JSON)
            data_str = data.to_json()  # Adjust based on your data structure

            # Store data in Redis
            self.redis_client.set(key, data_str)

            self.logger.info(f"Stored data for {resource} in Redis.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to store data in Redis: {e}")
            return False