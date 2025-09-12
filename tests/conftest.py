"""Pytest fixtures for unit tests."""

import pytest


@pytest.fixture(autouse=True)
def set_dummy_env(monkeypatch):
    """Automatically set dummy environment variables for CLIENT_ID and CLIENT_SECRET.

    Args:
        monkeypatch (pytest.MonkeyPatch): Fixture to modify environment variables.
    """
    monkeypatch.setenv("CLIENT_ID", "dummy_id")
    monkeypatch.setenv("CLIENT_SECRET", "dummy_secret")
