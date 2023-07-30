from datetime import datetime

import requests


class Vacancy:
    """Класс, характеризующий параметры вакансии"""

    def __init__(self, title: str, url: str, salary: dict, pub_date: str, requirements: str):
        """
        Инициализация объекта Vacancy.

        :param title: Название вакансии.
        :param url: Ссылка на вакансию.
        :param salary: Зарплата по вакансии
        (в формате словаря {'min': int, 'max': int, 'currency': str}).
        :param pub_date: Дата размещения вакансии.
        :param requirements: Требования к вакансии.
        """

        self.__title = self.check_title(title)
        self.__url = self.check_url(url)
        self.__salary = self.check_salary(salary)
        self.__pub_date = self.check_date_pub(pub_date)
        self.__requirements = self.check_requirements(requirements)

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    @property
    def salary(self):
        return self.__salary

    @property
    def medium_salary(self):
        return round((self.salary['min'] + self.salary['max']) / 2)

    @property
    def pub_date(self):
        return self.__pub_date

    @property
    def requirements(self):
        return self.__requirements

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        # return f'Вакансия {self.title} от {self.__pub_date}, ' \
        #        f'зарплата {self.salary["min"]}-{self.salary["max"]} {self.salary["currency"]}'

        return f'Вакансия "{self.title}" от {self.__pub_date}, зарплата от {self.salary["min"]} ' \
               f'до {self.salary["max"]} {self.salary["currency"]}'

    def __repr__(self) -> str:
        """Репрезентация класса для отладки"""
        return f"Vacancy({self.__dict__()})"

    def __dict__(self):
        return {
            'title': self.title,
            'url': self.url,
            'salary': self.salary,
            'pub_date': self.pub_date,
            'requirements': self.requirements
        }

    def __gt__(self, other: 'Vacancy') -> bool:
        """Проверяет больше ли средняя зарплата вакансии в отличие от другой"""
        return self.medium_salary > other.medium_salary
        # return self.salary > other.salary
    #
    # @salary.setter
    # def salary(self, value: dict) -> None:
    #     """Сеттер зарплаты вакансии"""
    #     self.__salary = self.check_salary(value)

    @staticmethod
    def check_title(title: str) -> str:
        """Проверяет есть ли название у вакансии"""
        if title:
            return title
        else:
            raise Exception('Пустое название вакансии')

    @staticmethod
    def check_url(url: str) -> str:
        """Проверяет валидна ли ссылка на вакансию"""
        status_code = requests.get(url=url).status_code
        if status_code == 200:
            return url
        raise Exception(f'Неверная ссылка, status code {status_code}')

    @staticmethod
    def check_salary(salary: dict) -> dict:
        """Проверяет валидна ли зарплата вакансии"""
        if salary:
            if salary['min'] and salary['max'] and salary['currency']:
                if salary['min'] <= salary['max']:
                    return salary
                else:
                    max_salary = salary['min']
                    salary['min'] = salary['max']
                    salary['max'] = max_salary
                    return salary
            else:
                return {}
        raise Exception(f'Одно или оба поля зарплаты не заполнены, {salary}')

    @staticmethod
    def check_date_pub(pub_date: str) -> str:
        """Проверяет валидна ли дата публикации"""
        if pub_date == str(datetime.fromisoformat(pub_date).date()):
            return pub_date
        raise Exception('Неверный формат даты')

    @staticmethod
    def check_requirements(requirements: str) -> str:
        """Проверяет валидны ли требования к вакансии"""
        if requirements:
            return requirements
        raise Exception('Требования отсутствуют')

    def check_data(self) -> bool:
        """Проверяет валидны ли все данные вакансии"""
        if not all([self.title, self.url, self.salary, self.pub_date, self.requirements]):
            return False
        raise Exception('Некоторые атрибуты вакансии не заданы')
