"""
Тестирование функций клиента для получения новостей.
"""

import pytest

from clients.news import NewsClient
from settings import API_KEY_NEWS


@pytest.mark.asyncio
class TestClientNews:
    """
    Тестирование клиента для получения новостей.
    """

    base_url = "https://newsapi.org/v2"

    @pytest.fixture
    def client(self):
        return NewsClient()

    async def test_get_base_url(self, client):
        assert await client.get_base_url() == self.base_url

    async def test_get_news(self, mocker, client):
        mocker.patch("clients.country.CountryClient._request")
        await client.get_news()
        client._request.assert_called_once_with(
            f"{self.base_url}/everything?q=Russia&sortBy=publishedAt&pageSize=3&apiKey={API_KEY_NEWS}"
        )

        await client.get_news("test")
        client._request.assert_called_with(
            f"{self.base_url}/everything?q=test&sortBy=publishedAt&pageSize=3&apiKey={API_KEY_NEWS}"
        )
