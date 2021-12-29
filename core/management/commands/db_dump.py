from django.core.management import BaseCommand

from core.models import Company, Vacancy, Specialty
from data import jobs, specialties, companies


class Command(BaseCommand):
    help = 'Наполняет базу данными из mock-файла data.py'

    def _populating_company(self, item_list=None):
        if isinstance(item_list, list) and item_list:
            count = 0
            for item in item_list:
                obj, created = Company.objects.update_or_create(
                    id=item['id'],
                    name=item['title'],
                    location=item['location'],
                    logo='/company_images/' + item['logo'],
                    description=item['description'],
                    employee_count=int(item['employee_count'])
                )
                if created:
                    count += 1
            self.stdout.write(self.style.SUCCESS(f'{count} компаний было добавлено'))
        else:
            self.stdout.write(self.style.ERROR('Произошла ошибка при создании компаний'))

    def _populating_specialty(self, item_list=None):
        if isinstance(item_list, list) and item_list:
            count = 0
            for item in item_list:
                obj, created = Specialty.objects.update_or_create(
                    code=item['code'],
                    title=item['title'],
                    picture='/specialties_images/' + item['logo'],
                )
                if created:
                    count += 1
            self.stdout.write(self.style.SUCCESS(f'{count} специальностей было добавлено'))
        else:
            self.stdout.write(self.style.ERROR('При создании специальностей произошла ошибка'))

    def _populating_vacancy(self, item_list=None):
        if isinstance(item_list, list) and item_list:
            count = 0
            for item in item_list:
                obj, created = Vacancy.objects.update_or_create(
                    title=item['title'],
                    specialty=Specialty.objects.get(code=item['specialty']),
                    company=Company.objects.get(pk=item['company']),
                    skills=item['skills'],
                    description=item['description'],
                    salary_min=int(item['salary_from']),
                    salary_max=int(item['salary_to'])
                )
                if created:
                    count += 1
            self.stdout.write(self.style.SUCCESS(f'{count} вакансий было добавлено'))
        else:
            self.stdout.write(self.style.ERROR('При создании вакансий произошла ошибка'))

    def handle(self, *args, **options):
        self._populating_company(companies)
        self._populating_specialty(specialties)
        self._populating_vacancy(jobs)
