from abc import ABC, abstractmethod


class BaseAPI(ABC):
    def __init__(self, base_url: str):
        """Инициализация базового класса для API"""
        self._base_url = base_url

    @abstractmethod
    def get_vacancies(self, keyword: str, vacancies_amount: int) -> list:
        """Возвращает список найденных вакансий по ключевому слову"""
        pass

    @staticmethod
    def get_title(vacancy) -> str:
        pass

    @staticmethod
    def get_url(vacancy) -> str:
        pass

    @staticmethod
    def get_salary(vacancy) -> dict:
        pass

    @staticmethod
    def get_pub_date(vacancy) -> str:
        pass

    @staticmethod
    def get_requirements(vacancy) -> str:
        pass
