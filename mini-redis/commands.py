#this file handles parsing and executing commands

def handle_set(parts, store):
    if len(parts) < 3:
        return "ERR wrong number of arguments for SET"
    key = parts[1]
    value = " ".join(parts[2:])
    return store.set(key, value)

def handle_get(parts,store):
        if len(parts)!=2:
            return "ERR wrong number of arguments for GET"
        key=parts[1]
        return store.get(key)

def handle_delete(parts,store):
    if len(parts)!=2:
        return "ERR wrong number of arguments for DELETE"
    key=parts[1]
    return store.delete(key)

def handle_exists(parts,store):
    if len(parts)!=2:
        return "ERR wrong number of arguments for EXISTS"
    key=parts[1]
    return store.exists(key)

COMMANDS = {
    "SET": handle_set,
    "GET": handle_get,
    "DELETE": handle_delete,
    "EXISTS": handle_exists,
}
def execute_command(command_line, store):
    parts=command_line.strip().split()
    if not parts:
        return "ERR empty command"

    command = parts[0].upper()
    parts[0] = command

    handler = COMMANDS.get(command)

    if handler is None:
        return f"ERR unknown command '{command}'"

    return handler(parts, store)