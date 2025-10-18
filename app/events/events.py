import pika
import json
import logging
import uuid
from enum import Enum

from app.core.config import settings

logger = logging.getLogger(__name__)

class NotificationEventType(str, Enum):
    COMMENT_CREATED = "COMMENT_CREATED"
    REACTION_ADDED = "REACTION_ADDED"

class NotificationEventPublisher:
    @staticmethod
    def publish_comment_created(
        channel: pika.channel.Channel,
        post_owner_id: uuid.UUID,
        commenter_id: uuid.UUID,
        post_id: uuid.UUID,
        comment_id: uuid.UUID,
    ) -> bool:

        if post_owner_id == commenter_id:
            logger.debug(f"Skipping self-notification: user {commenter_id} commented on own post")
            return True

        event = {
            "type": NotificationEventType.COMMENT_CREATED.value,
            "user_id": str(post_owner_id),
            "actor_id": str(commenter_id),
            "post_id": str(post_id),
            "comment_id": str(comment_id),
            "message": f"{comment_id} commented on your post."
        }

        return NotificationEventPublisher._publish_event(channel, event)

    @staticmethod
    def publish_reaction_added(
        channel: pika.channel.Channel,
        post_owner_id: uuid.UUID,
        reactor_id: uuid.UUID,
        post_id: uuid.UUID,
    ) -> bool:

        if post_owner_id == reactor_id:
            logger.debug(f"Skipping self-notification: user {reactor_id} reacted to own post")
            return True

        event = {
            "type": NotificationEventType.REACTION_ADDED.value,
            "user_id": str(post_owner_id),
            "actor_id": str(reactor_id),
            "post_id": str(post_id),
            "message": f"{reactor_id} reacted to your post."
        }

        return NotificationEventPublisher._publish_event(channel, event)

    @staticmethod
    def _publish_event(channel: pika.channel.Channel, event: dict) -> bool:
        try:
            body = json.dumps(event)

            channel.basic_publish(
                exchange="",
                routing_key=settings.MQ_QUEUE,
                body=body,
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=2
                )
            )

            logger.info(f"Published {event['type']} event for user {event['user_id']}")
            return True

        except Exception as e:
            logger.error(f"Failed to publish notification event: {e}")
            return False
