"""
Функции для формирования выходной информации.
"""

from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from prettytable import PrettyTable

from collectors.models import LocationInfoDTO


class Renderer:
    """
    Генерация результата преобразования прочитанных данных.
    """

    def __init__(self, location_info: LocationInfoDTO) -> None:
        """
        Конструктор.

        :param location_info: Данные о географическом месте.
        """

        self.location_info = location_info

    async def render(self) -> tuple[str, ...]:
        """
        Форматирование прочитанных данных.

        :return: Результат форматирования
        """
        result = "Информация о стране\n"
        base_table = PrettyTable()
        base_table.field_names = ["Характеристика", "Значение"]
        base_table.add_row(["Страна", self.location_info.location.name])
        base_table.add_row(["Столица", self.location_info.location.capital])
        base_table.add_row(["Регион", self.location_info.location.subregion])
        base_table.add_row(["Площадь", f"{self.location_info.location.area} кв. км."])
        base_table.add_row(["Широта", self.location_info.location.latitude])
        base_table.add_row(["Долгота", self.location_info.location.longitude])
        base_table.add_row(["Языки", await self._format_languages()])
        base_table.add_row(["Население", await self._format_population()])
        base_table.add_row(["Курсы валют", await self._format_currency_rates()])

        result += str(base_table) + "\n\nИнформация о погоде\n"

        weather_table = PrettyTable()
        weather_table.field_names = ["Характеристика", "Значение"]
        weather_table.add_row(["Температура", f"{self.location_info.weather.temp} °C"])
        weather_table.add_row(["Описание", self.location_info.weather.description])
        weather_table.add_row(["Видимость", f"{self.location_info.location.subregion} м."])
        weather_table.add_row(["Скорость ветра", f"{self.location_info.location.area} м/с"])

        result += str(weather_table) + "\n\nИнформация о времени\n"

        time_table = PrettyTable()
        time_table.field_names = ["Характеристика", "Значение"]
        time_table.add_row(["Часовой пояс", f"UTC+{self.location_info.weather.timezone // 3600 }"])
        time_table.add_row(["Местное время",
                               datetime.fromtimestamp(self.location_info.weather.dt + self.location_info.weather.timezone).strftime('%d.%m.%Y %H:%M')])

        result += str(time_table) + "\n"

        return (
            result,
            f"{await self._format_news()}",
        )

    async def _format_languages(self) -> str:
        """
        Форматирование информации о языках.

        :return:
        """

        return ", ".join(
            f"{item.name} ({item.native_name})"
            for item in self.location_info.location.languages
        )

    async def _format_population(self) -> str:
        """
        Форматирование информации о населении.

        :return:
        """

        # pylint: disable=C0209
        return "{:,}".format(self.location_info.location.population).replace(",", ".")

    async def _format_currency_rates(self) -> str:
        """
        Форматирование информации о курсах валют.

        :return:
        """

        return ", ".join(
            f"{currency} = {Decimal(rates).quantize(exp=Decimal('.01'), rounding=ROUND_HALF_UP)} руб."
            for currency, rates in self.location_info.currency_rates.items()
        )

    async def _format_news(self) -> str:
        """
        Форматирование новостей.

        :return:
        """
        result = "\nНовости\n"
        for news in self.location_info.news:
            table = PrettyTable()
            table.field_names = ["Характеристика", "Значение"]
            table._max_width = {"Характеристика": 50, "Значение": 120}
            table.align["Значение"] = "l"
            table.add_row(["Источник", news.source])
            table.add_row(["Автор", news.author])
            table.add_row(["Название", news.title])
            table.add_row(["Описание", news.description])
            table.add_row(["Ссылка", news.url])
            table.add_row(["Дата публикации", news.publishedAt])
            table.add_row(["Текст", news.content])
            result += str(table) + "\n"

        return result
