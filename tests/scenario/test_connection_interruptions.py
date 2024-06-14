import pytest

from redis import Redis


from ..conftest import _get_client
from . import get_endpoint
from .fake_app import FakeApp


@pytest.fixture
def endpoint_name():
    return "re-standalone"


@pytest.fixture
def client(request: pytest.FixtureRequest, endpoint_name: str):
    e = get_endpoint(request, endpoint_name)

    r = _get_client(Redis, request, decode_responses=True, from_url=e.url)
    r.flushdb()
    return r


def test_connection_interruptions(client: Redis):
    # TBD: Implement test_connection_interruptions
    # FakeApp(client, lambda c: c.set("foo", "bar")).run()
    pass
