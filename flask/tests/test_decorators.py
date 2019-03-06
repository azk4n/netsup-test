#!/usr/bin/python3
import pytest
from app import app


@pytest.yield_fixture
def client():
    client = app.test_client()

    yield client


def test_without_authorization(client):
    response = client.get("/ping")
    assert 401 == response.status_code


def test_with_authorization(client):
    response = client.get("/ping", headers={"Authorization": "test"})
    assert 200 == response.status_code
