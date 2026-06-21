import hashlib
import json
import time
from functools import wraps
import logging
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)

# Global config flag for hackathon demo manipulation
CACHE_ENABLED = True

class CacheManager:
    _store: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        if not CACHE_ENABLED:
            return None
        
        record = cls._store.get(key)
        if not record:
            return None
            
        if time.time() > record["expires_at"]:
            del cls._store[key]
            return None
            
        return record["value"]

    @classmethod
    def set(cls, key: str, value: Any, ttl_seconds: int = 300) -> None:
        if not CACHE_ENABLED:
            return
            
        cls._store[key] = {
            "value": value,
            "expires_at": time.time() + ttl_seconds
        }

    @classmethod
    def clear(cls) -> None:
        cls._store.clear()


def generate_cache_key(func_name: str, args: tuple, kwargs: dict) -> str:
    # Serialize args/kwargs safely, ignoring non-serializables for this simple implementation
    try:
        # Ensure we don't accidentally cache PII by avoiding complex object serialization
        # We only cache primitives (strings, ints, floats)
        safe_args = [a for a in args if isinstance(a, (str, int, float, bool))]
        safe_kwargs = {k: v for k, v in kwargs.items() if isinstance(v, (str, int, float, bool))}
        
        key_dict = {"func": func_name, "args": safe_args, "kwargs": safe_kwargs}
        key_str = json.dumps(key_dict, sort_keys=True)
        return hashlib.sha256(key_str.encode('utf-8')).hexdigest()
    except Exception as e:
        logger.warning(f"Failed to generate cache key for {func_name}: {e}")
        return str(time.time()) # Fallback: never hit cache


def cached(ttl_seconds: int = 300):
    """
    A decorator to cache function outputs in-memory.
    Use carefully to avoid massive memory bloat.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not CACHE_ENABLED:
                return func(*args, **kwargs)
                
            cache_key = generate_cache_key(func.__name__, args, kwargs)
            cached_value = CacheManager.get(cache_key)
            
            if cached_value is not None:
                logger.info(f"Cache HIT for {func.__name__}")
                return cached_value
                
            logger.info(f"Cache MISS for {func.__name__}")
            result = func(*args, **kwargs)
            CacheManager.set(cache_key, result, ttl_seconds)
            return result
            
        return wrapper
    return decorator
