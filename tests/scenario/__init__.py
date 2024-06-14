import json
import os.path
import dataclasses

import pytest
from urllib.parse import urlparse


@dataclasses.dataclass
class Endpoint:
    bdb_id: int
    username: str
    password: str
    tls: bool
    endpoints: list[str]

    @property
    def url(self):
        parsed_url = urlparse(self.endpoints[0])

        if self.tls:
            parsed_url._replace(scheme="rediss")

        parsed_url._replace(username=self.username, password=self.password)

        return parsed_url.geturl()


def get_endpoint(request: pytest.FixtureRequest, endpoint_name: str) -> Endpoint:
    endpoints_config_path = request.config.getoption("--endpoints-config")

    if not (endpoints_config_path and os.path.exists(endpoints_config_path)):
        raise ValueError(f"Endpoints config file not found: {endpoints_config_path}")

    try:
        with open(endpoints_config_path, "r") as f:
            endpoints_config = json.load(f)
    except Exception as e:
        raise ValueError(
            f"Failed to load endpoints config file: {endpoints_config_path}"
        ) from e

    if not (isinstance(endpoints_config, dict) and endpoint_name in endpoints_config):
        raise ValueError(f"Endpoint not found in config: {endpoint_name}")

    return Endpoint(**endpoints_config.get(endpoint_name))


