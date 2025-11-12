import logging
from typing import Callable, Any

from app.core.exceptions import AppError

logger = logging.getLogger(__name__)

def handle_service_call(service_func: Callable, *args, **kwargs) -> Any:
    try:
        return service_func(*args, **kwargs)
    except AppError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in {service_func.__name__}: {e}", exc_info=True)
        raise AppError()

async def handle_service_call_async(service_func: Callable, *args, **kwargs) -> Any:
    try:
        return await service_func(*args, **kwargs)
    except AppError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in {service_func.__name__}: {e}", exc_info=True)
        raise AppError()