import os

import pytest
import requests

class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url(self):
        """ Get the API Gateway URL from environmental variable."""

        return os.environ.get("API_URL")

    def test_api_gateway(self, api_gateway_url):
        """ Call the API Gateway endpoint and check the response """
        response = requests.get(api_gateway_url)

        assert response.status_code == 200
        assert response.json() == {"message": "hello world"}
