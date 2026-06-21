import time
from verdaterrakai.app.caching import CacheManager, cached

call_count = 0

@cached(ttl_seconds=1)
def side_effect_func(a):
    global call_count
    call_count += 1
    return a * 2

def test_decorator_caches_outputs():
    global call_count
    call_count = 0
    CacheManager.clear()
    
    v1 = side_effect_func(10)
    v2 = side_effect_func(10)
    
    assert v1 == 20
    assert v2 == 20
    assert call_count == 1  # Cache HIT
    
    # Different argument
    v3 = side_effect_func(5)
    assert v3 == 10
    assert call_count == 2

def test_cache_ttl_expiration():
    global call_count
    call_count = 0
    CacheManager.clear()
    
    side_effect_func(100)
    assert call_count == 1
    
    # Force sleep over TTL
    time.sleep(1.1)
    
    side_effect_func(100)
    assert call_count == 2  # TTL Expired, should miss cache
