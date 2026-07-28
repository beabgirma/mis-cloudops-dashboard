from store import MiniRedisStore


def test_set_and_get_value():
    store = MiniRedisStore()

    result = store.set("name", "beab")

    assert result == "OK"
    assert store.get("name") == "beab"


def test_get_missing_key_returns_nil():
    store = MiniRedisStore()

    assert store.get("missing") == "(nil)"


def test_delete_existing_key():
    store = MiniRedisStore()
    store.set("language", "python")

    result = store.delete("language")

    assert result == "OK"
    assert store.get("language") == "(nil)"


def test_delete_missing_key_returns_nil():
    store = MiniRedisStore()

    assert store.delete("missing") == "(nil)"


def test_exists_returns_1_when_key_exists():
    store = MiniRedisStore()
    store.set("name", "beab")

    assert store.exists("name") == "1"


def test_exists_returns_0_when_key_does_not_exist():
    store = MiniRedisStore()

    assert store.exists("missing") == "0"