from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def redis_client(monkeypatch):
    monkeypatch.delenv("REDIS_LEADER_SERVICE_HOST", raising=False)
    monkeypatch.delenv("REDIS_FOLLOWER_SERVICE_HOST", raising=False)
    client = Mock()
    monkeypatch.setattr(main.redis, "Redis", Mock(return_value=client))
    return client


@pytest.fixture
def client(redis_client):
    with TestClient(main.app) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_messages_returns_empty_list_when_redis_is_empty(client, redis_client):
    redis_client.get.return_value = None

    response = client.get("/api/messages")

    assert response.status_code == 200
    assert response.json() == {"messages": []}
    main.redis.Redis.assert_called_once_with(
        host="redis-follower",
        port=6379,
        decode_responses=True,
    )
    redis_client.get.assert_called_once_with("guestbook")


def test_get_messages_returns_saved_messages(client, redis_client):
    redis_client.get.return_value = "hello,world"

    response = client.get("/api/messages")

    assert response.status_code == 200
    assert response.json() == {"messages": ["hello", "world"]}


def test_add_message_creates_message_list(client, redis_client):
    redis_client.get.return_value = None

    response = client.post("/api/messages", params={"message": "hello"})

    assert response.status_code == 200
    assert response.json() == {"status": "updated"}
    main.redis.Redis.assert_called_once_with(
        host="redis-leader",
        port=6379,
        decode_responses=True,
    )
    redis_client.get.assert_called_once_with("guestbook")
    redis_client.set.assert_called_once_with("guestbook", "hello")


def test_add_message_appends_to_existing_messages(client, redis_client):
    redis_client.get.return_value = "hello"

    response = client.post("/api/messages", params={"message": "world"})

    assert response.status_code == 200
    assert response.json() == {"status": "updated"}
    redis_client.set.assert_called_once_with("guestbook", "hello,world")
