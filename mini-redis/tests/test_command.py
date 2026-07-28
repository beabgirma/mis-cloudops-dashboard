

from commands import execute_command
from store import MiniRedisStore

def test_set_command():
    store=MiniRedisStore()
    result=execute_command("SET name beab",store)
    assert result=="OK"
    assert store.get("name")=="beab"

def test_get_command():
    store=MiniRedisStore()
    store.set("name", "beab")
    result=execute_command("GET name",store)
    assert store.get("name")=="beab"

def test_delete_command():
    store=MiniRedisStore()
    store.set("name","beab")
    result=execute_command("DELETE name",store)
    assert result=="OK"
    assert store.get("name")=="(nil)"

def test_exists_command():
    store=MiniRedisStore()
    store.set("name","beab")
    result=execute_command("EXISTS name",store)
    assert result=="1"

def test_unknown_command():
    store=MiniRedisStore()
    result=execute_command("UNKNOWN name",store)
    assert result=="ERR unknown command 'UNKNOWN'"

def test_empty_command():
    store=MiniRedisStore()
    result=execute_command("",store)
    assert result=="ERR empty command"

