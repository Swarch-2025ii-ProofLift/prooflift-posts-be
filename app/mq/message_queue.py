import aio_pika
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class MQConnection:
    def __init__(self):
        self._connection: Optional[aio_pika.Connection] = None
        self._channel: Optional[aio_pika.Channel] = None

    async def connect(self) -> aio_pika.Channel:
        try:
            connection_url = f"amqp://{settings.MQ_USER}:{settings.MQ_PASSWORD}@{settings.MQ_HOST}:{settings.MQ_PORT}/"

            self._connection = await aio_pika.connect_robust(
                connection_url,
                heartbeat=600,
                connection_attempts=5,
                retry_delay=2
            )

            self._channel = await self._connection.channel()

            # Declare queue as durable
            await self._channel.declare_queue(
                settings.MQ_QUEUE,
                durable=True
            )

            logger.info(f"Connected to MQ at {settings.MQ_HOST}:{settings.MQ_PORT}")
            return self._channel

        except Exception as e:
            logger.error(f"Failed to connect to MQ: {e}")
            raise

    async def get_channel(self) -> aio_pika.Channel:
        if not self._channel or self._channel.is_closed:
            return await self.connect()
        return self._channel

    async def close(self):
        try:
            if self._channel and not self._channel.is_closed:
                await self._channel.close()
            if self._connection and not self._connection.is_closed:
                await self._connection.close()
            logger.info("MQ connection closed")
        except Exception as e:
            logger.error(f"Error closing MQ connection: {e}")

mq_connection = MQConnection()

async def get_mq_channel() -> aio_pika.Channel:
    return await mq_connection.get_channel()
