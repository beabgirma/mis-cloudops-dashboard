import time
from store import MiniRedisStore


def test_key_expires_after_ttl(tmp_path):
    file_path = tmp_path / "test_data.json"

    store = MiniRedisStore(file_path)
    store.set("token", "abc123")
    store.expire("token", 1)

    assert store.get("token") == "abc123"

    time.sleep(1.1)

    assert store.get("token") == "(nil)"


def test_ttl_returns_seconds_left(tmp_path):
    file_path = tmp_path / "test_data.json"

    store = MiniRedisStore(file_path)
    store.set("token", "abc123")
    store.expire("token", 10)

    ttl = store.ttl("token")

    assert ttl > 0
    assert ttl <= 10


def test_expire_missing_key_returns_zero(tmp_path):
    file_path = tmp_path / "test_data.json"

    store = MiniRedisStore(file_path)

    assert store.expire("missing", 10) == 0