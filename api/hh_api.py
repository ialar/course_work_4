from datetime import datetime

import requests

from api.base_api import BaseAPI
from src.exception import ParsingError
from src.vacancy import Vacancy


class HeadHunter(BaseAPI):
    """Подкласс для поиска вакансий на HeadHunter"""
    url: str = 'https://api.hh.ru/vacancies'

    def __init__(self, url: str = url):
        """Инициализация подкласса HeadHunter"""
        super().__init__(url)

    def get_vacancies(self, keyword: str, vacancies_amount: int = 50) -> list:
        params = {
            'text': keyword,
            'per_page': vacancies_amount,
            'page': None,
            'archived': False,
            'only_with_salary': True
        }
        response_json = requests.get(url=self._base_url, params=params).json()
        vacancies = []

        try:
            for item in response_json.get("items", []):
                vacancy = Vacancy(title=self.get_title(item), url=self.get_url(item), salary=self.get_salary(item),
                                  pub_date=self.get_date_pub(item), requirements=self.get_requirements(item))
                vacancies.append(vacancy)
        except ParsingError as error:
            print(error)
        return vacancies

    @staticmethod
    def get_title(vacancy) -> str:
        return vacancy['name']

    @staticmethod
    def get_url(vacancy) -> str:
        return vacancy['url']

    @staticmethod
    def get_salary(vacancy) -> dict:
        salary = {'min': int(vacancy['salary']['from']), 'currency': vacancy['salary']['currency']}
        if vacancy['salary']['to'] is None:
            salary['max'] = salary['min']
        salary['max'] = int(vacancy['salary']['from'])
        return salary

    @staticmethod
    def get_date_pub(vacancy) -> str:
        return str(datetime.fromisoformat(vacancy['published_at'][:10]).date())

    @staticmethod
    def get_requirements(vacancy) -> str:
        return vacancy['snippet']['requirement']
