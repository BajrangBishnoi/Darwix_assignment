# tests/test_services.py

import pytest

from app.crud import CallService
from app.schema import CallBase


class FakeDBSession:
    def get(self, model, call_id):
        return None


def test_get_call_by_id_returns_none():
    db = FakeDBSession()
    service = CallService(db)
    result = service.get_call_by_id("nonexistent-id")
    assert result is None
