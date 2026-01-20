import time

# Giả lập Redis trong RAM
_fake_redis = {}

def check_cache(key: str):
    if key in _fake_redis:
        print(f"--- Cache HIT cho key: {key} ---")
        return _fake_redis[key]
    print(f"--- Cache MISS cho key: {key} ---")
    return None

def save_cache(key: str, value: dict):
    # Lưu cache
    _fake_redis[key] = value