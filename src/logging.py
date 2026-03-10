import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        user = data.get("event_from_user")
        chat = data.get("event_chat")

        handler_obj = data.get("handler")
        handler_name = handler_obj.callback.__name__ if handler_obj else "unknown"

        logger.info(
            f"Handler: {handler_name} | "
            f"User: {user.id if user else 'Unknown'} | "
            f"Chat: {chat.id if chat else 'Unknown'} | "
            f"Event: {event.__class__.__name__}"
        )

        return await handler(event, data)
