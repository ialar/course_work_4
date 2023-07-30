import os
from datetime import datetime

import requests

from api.base_api import BaseAPI
from src.exception import ParsingError
from src.vacancy import Vacancy


class SuperJob(BaseAPI):
    """Подкласс для поиска вакансий на SuperJob"""
    url: str = 'https://api.superjob.ru/2.0'

    def __init__(self, url: str = url):
        """Инициализация подкласса SuperJob"""
        super().__init__(url)

    def get_vacancies(self, keyword: str, vacancies_amount: int = 50) -> list:
        url = f'{self._base_url}/vacancies/'
        headers = {
            'X-Api-App-Id': os.getenv('SuperJob_API')
        }
        params = {
            "keywords": [[1, keyword]],
            "count": vacancies_amount,
            'page': None,
            'archive': False
        }
        response_json = requests.get(url, headers=headers, params=params).json()
        vacancies = []

        try:
            for item in response_json.get("objects", []):
                vacancy = Vacancy(title=self.get_title(item), url=self.get_url(item), salary=self.get_salary(item),
                                  pub_date=self.get_date_pub(item), requirements=self.get_requirements(item))
                vacancies.append(vacancy)
        except ParsingError as error:
            print(error)
        return vacancies

    @staticmethod
    def get_title(vacancy) -> str:
        return vacancy['profession']

    @staticmethod
    def get_url(vacancy) -> str:
        return vacancy['link']

    @staticmethod
    def get_salary(vacancy) -> dict:
        salary = {'min': int(vacancy['payment_from']), 'currency': vacancy['currency']}
        if salary['min'] is None:
            salary['min'] = 0
        if vacancy['payment_to'] == (None or 0):
            salary['max'] = salary['min']
        else:
            salary['max'] = int(vacancy['payment_to'])
        return salary

    @staticmethod
    def get_date_pub(vacancy) -> str:
        return str(datetime.utcfromtimestamp(vacancy["date_published"]).date())

    @staticmethod
    def get_requirements(vacancy) -> str:
        return vacancy['candidat']
