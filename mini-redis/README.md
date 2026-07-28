# Mini Redis

Mini Redis is a small Redis-inspired key-value database built in Python.

It lets users store, retrieve, delete, and expire data using simple commands like:

```bash
SET name beab
GET name
DELETE name
EXPIRE token 10
TTL token
```

The goal of this project was to understand how backend database tools work under the hood, including storage, command handling, persistence, testing, and key expiration.

---

## Features

- Store key-value data
- Get values by key
- Delete keys
- Check if a key exists
- Save data to a JSON file
- Load saved data after restart
- Expire keys automatically with TTL
- Test coverage with pytest

---

## Example Commands

```bash
SET name beab
```

Returns:

```bash
OK
```

```bash
GET name
```

Returns:

```bash
beab
```

```bash
DELETE name
```

Returns:

```bash
OK
```

```bash
GET name
```

Returns:

```bash
(nil)
```

```bash
SET token abc123
EXPIRE token 10
TTL token
```

The key `token` will automatically expire after 10 seconds.

---

## Project Structure

```bash
mini-redis/
├── client.py
├── server.py
├── commands.py
├── store.py
├── data.json
├── tests/
│   ├── test_command.py
│   ├── test_store.py
│   ├── test_persistence.py
│   └── test_ttl.py
├── requirements.txt
└── README.md
```

---

## How to Run

Clone the repo:

```bash
git clone https://github.com/beabgirma/mini-redis.git
cd mini-redis
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
python server.py
```

In another terminal, run the client:

```bash
python client.py
```

---

## Running Tests

Run the full test suite:

```bash
pytest
```

---

## What I Learned

While building this project, I learned about:

- How key-value databases work
- Python dictionaries for in-memory storage
- Reading and writing JSON files
- Client-server communication
- Writing automated tests with pytest
- Git branches and pull requests
- GitHub Actions for automated testing
- Implementing TTL expiration logic

---

## Tech Stack

- Python
- Pytest
- JSON
- GitHub Actions
- Git / GitHub

---

## Status

This project is complete and portfolio-ready.