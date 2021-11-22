from django.core.management import BaseCommand

from IT_hunter.models import Company, Vacancy, Specialty


""" Вакансии """

jobs = [

    {"title": "Разработчик на Python", "cat": "backend", "company": "staffingsmarter", "salary_from": "100000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик в проект на Django", "cat": "backend", "company": "swiftattack", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик на Swift в аутсорс компанию", "cat": "backend", "company": "swiftattack",
     "salary_from": "120000", "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Мидл программист на Python", "cat": "backend", "company": "workiro", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Питонист в стартап", "cat": "backend", "company": "primalassault", "salary_from": "120000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"}

]

""" Компании """

companies = [

    {"title": "workiro"},
    {"title": "rebelrage"},
    {"title": "staffingsmarter"},
    {"title": "evilthreath"},
    {"title": "hirey"},
    {"title": "swiftattack"},
    {"title": "troller"},
    {"title": "primalassault"}

]

""" Категории """

specialties = [

    {"code": "frontend", "title": "Фронтенд"},
    {"code": "backend", "title": "Бэкенд"},
    {"code": "gamedev", "title": "Геймдев"},
    {"code": "devops", "title": "Девопс"},
    {"code": "design", "title": "Дизайн"},
    {"code": "products", "title": "Продукты"},
    {"code": "management", "title": "Менеджмент"},
    {"code": "testing", "title": "Тестирование"}

]


class Command(BaseCommand):
    help = 'Populating the database'

    @staticmethod
    def _populating_company(self, item_list=None):
        if isinstance(item_list, list) and item_list:
            count = 0
            for item in item_list:
                Company.objects.create(
                    id=item['id'],
                    name=item['title'],
                    location=item['location'],
                    logo=item['logo'],
                    description=item['description'],
                    employee_count=int(item['employee_count'])
                )
                count += 1
            print(f'{count} объектов было добавлено')

    @staticmethod
    def _populating_specialty(self, item_list=None):
        if isinstance(item_list, list) and item_list:
            count = 0
            for item in item_list:
                Specialty.objects.create(
                    code=item['code'],
                    title=item['title'],
                )
                count += 1
            print(f'{count} объектов было добавлено')

    @staticmethod
    def _populating_vacancy(self, item_list=None):
        if isinstance(item_list, list) and item_list:
            count = 0
            for item in item_list:
                Vacancy.objects.create(
                    id=item['id'],
                    title=item['title'],
                    specialty=Specialty.objects.get(code=item['specialty']),
                    company=Company.objects.get(pk=item['company']),
                    skills=item['skills'],
                    description=item['description'],
                    salary_min=int(item['salary_from']),
                    salary_max=int(item['salary_to'])
                )
                count += 1
            print(f'{count} объектов было добавлено')

    def handle(self, *args, **options):
        self._populating_company(self, item_list=companies)
        self._populating_specialty(self, item_list=specialties)
        self._populating_vacancy(self, item_list=jobs)
