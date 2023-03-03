"""
Функции для взаимодействия с внешним сервисом-провайдером новостей.
"""
from http import HTTPStatus
from typing import Optional

import aiohttp

from clients.base import BaseClient
from logger import trace_config
from settings import API_KEY_NEWS


class NewsClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером новостей.
    """

    async def get_base_url(self) -> str:
        return "https://newsapi.org/v2"

    async def _request(self, endpoint: str) -> Optional[dict]:

        # формирование заголовков запроса
        headers = {"apikey": API_KEY_NEWS}

        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(endpoint, headers=headers) as response:
                if response.status == HTTPStatus.OK:
                    return await response.json()

                return None

    async def get_news(self, country: str = "Russia") -> Optional[dict]:
        """
        Получение новостей.

        :param country: Страна
        :return:
        """

        return await self._request(
            f"{await self.get_base_url()}/everything?q={country}&sortBy=publishedAt&pageSize=3&apiKey={API_KEY_NEWS}"
        )
