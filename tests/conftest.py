import pytest


@pytest.fixture(autouse=True)
def set_dummy_env(monkeypatch):
    monkeypatch.setenv("CLIENT_ID", "dummy_id")
    monkeypatch.setenv("CLIENT_SECRET", "dummy_secret")
