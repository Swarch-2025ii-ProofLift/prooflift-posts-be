from typing import Callable, Any

from app.core.exceptions import AppError

def handle_service_call(service_func: Callable, *args, **kwargs) -> Any:
    try:
        return service_func(*args, **kwargs)
    except AppError:
        raise
    except Exception:
        raise AppError()