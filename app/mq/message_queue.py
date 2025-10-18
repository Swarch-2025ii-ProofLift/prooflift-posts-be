import pika
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class MQConnection:
    def __init__(self):
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.channel.Channel] = None

    def connect(self) -> pika.channel.Channel:
        try:
            credentials = pika.PlainCredentials(
                settings.MQ_USER,
                settings.MQ_PASSWORD
            )
            parameters = pika.ConnectionParameters(
                host=settings.MQ_HOST,
                port=settings.MQ_PORT,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )

            self._connection = pika.BlockingConnection(parameters)
            self._channel = self._connection.channel()

            self._channel.queue_declare(
                queue=settings.MQ_QUEUE,
                durable=True
            )

            logger.info(f"Connected to MQ at {settings.MQ_HOST}:{settings.MQ_PORT}")
            return self._channel

        except Exception as e:
            logger.error(f"Failed to connect to MQ: {e}")
            raise

    def get_channel(self) -> pika.channel.Channel:
        if not self._channel or self._channel.is_closed:
            return self.connect()
        return self._channel

    def close(self):
        try:
            if self._channel and not self._channel.is_closed:
                self._channel.close()
            if self._connection and not self._connection.is_closed:
                self._connection.close()
            logger.info("MQ connection closed")
        except Exception as e:
            logger.error(f"Error closing MQ connection: {e}")

mq_connection = MQConnection()

def get_mq_channel() -> pika.channel.Channel:
    return mq_connection.get_channel()
