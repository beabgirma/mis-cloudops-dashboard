from store import MiniRedisStore


def test_store_persists_data_after_restart(tmp_path):
    file_path = tmp_path / "test_data.json"

    store = MiniRedisStore(file_path)
    store.set("name", "brook")

    restarted_store = MiniRedisStore(file_path)

    assert restarted_store.get("name") == "brook"


def test_delete_removes_data_from_saved_file(tmp_path):
    file_path = tmp_path / "test_data.json"

    store = MiniRedisStore(file_path)
    store.set("name", "brook")
    store.delete("name")

    restarted_store = MiniRedisStore(file_path)

    assert restarted_store.get("name") == "(nil)"
