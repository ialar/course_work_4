import json

from src.vacancy import Vacancy


class JSONSaver:
    """Класс для сохранения вакансий в файл"""

    def save_vacancies(self, filename: str, vacancies: [Vacancy]) -> None:
        """Сохраняет вакансии в файл"""
        try:
            existing_vacancies = self.get_vacancies(filename=filename)
            for vacancy in vacancies:
                if vacancy not in existing_vacancies:
                    existing_vacancies.append(vacancy)
            vacancies_to_save = [vacancy.__dict__() for vacancy in existing_vacancies]
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(vacancies_to_save, file, ensure_ascii=False, indent=2)

        except FileNotFoundError:
            vacancies_to_save = [vacancy.__dict__() for vacancy in vacancies]
            with open(filename, "x", encoding="utf-8") as file:
                json.dump(vacancies_to_save, file, ensure_ascii=False, indent=2)

    @staticmethod
    def get_vacancies(filename: str) -> [Vacancy]:
        """Возвращает список вакансий из заданного файла"""
        vacancies = []
        with open(filename, "r", encoding="utf-8") as file:
            vacancies_data = json.load(file)
            for vacancy_data in vacancies_data:
                vacancy = Vacancy(title=vacancy_data['title'], url=vacancy_data['url'],
                                  salary=vacancy_data['salary'], pub_date=vacancy_data['pub_date'],
                                  requirements=vacancy_data['requirements'])
                vacancies.append(vacancy)
        return vacancies
