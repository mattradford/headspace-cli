"""
Right now this only contains basic tests. Because the library depends heavily on
headspace, it makes it difficult to write automated tests.
"""

import base64
import json

import pytest

from pyheadspace import auth
from pyheadspace.__main__ import round_off


class FakeResponse:
    def __init__(self, text):
        self.text = text


def test_round_off_duration():
    assert round_off(1.1 * 60_000) == 1
    assert round_off(1.2 * 60_000) == 1
    assert round_off(1.9 * 60_000) == 1
    assert round_off(2 * 60_000) == 2
    assert round_off(2.5 * 60_000) == 2
    assert round_off(2.9 * 60_000) == 2
    assert round_off(3 * 60_000) == 3

    assert round_off(3.1 * 60_000) == 3
    assert round_off(3.9 * 60_000) == 3
    assert round_off(4 * 60_000) == 5
    assert round_off(5 * 60_000) == 5
    assert round_off(5.2 * 60_000) == 5
    assert round_off(6 * 60_000) == 5
    assert round_off(7 * 60_000) == 5
    assert round_off(10.2 * 60_000) == 10
    assert round_off(16 * 60_000) == 15


def test_get_client_id_retries_after_rate_limit(monkeypatch):
    responses = iter(
        [
            FakeResponse(
                "<html>We are sorry, an error occurred. The rate limit for endpoint /u/login/identifier was reached.</html>"
            ),
            FakeResponse(
                '<script>window.config = {"clientId":"retry-client-123"};</script>'
            ),
        ]
    )

    monkeypatch.setattr(auth.session, "get", lambda *args, **kwargs: next(responses))
    monkeypatch.setattr(auth.time, "sleep", lambda *_args, **_kwargs: None)

    assert auth.get_client_id() == "retry-client-123"


def test_get_client_id_decodes_base64_payload():
    payload = json.dumps({"client": {"id": "encoded-client-456"}}).encode()
    encoded = base64.b64encode(payload).decode("ascii")

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(
        auth.session,
        "get",
        lambda *args, **kwargs: FakeResponse(f'<script>var config = atob("{encoded}");</script>'),
    )
    try:
        assert auth.get_client_id() == "encoded-client-456"
    finally:
        monkeypatch.undo()
