import os
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from core.models import Vacancy, Specialty, Company


class VacancyModelTest(TestCase):
    """Тестирует поля модели Vacancy"""

    @classmethod
    def setUpTestData(cls):
        specialty = Specialty.objects.create(
            code='specialty_code', title='specialty_title',
        )
        company = Company.objects.create(
            name='company_name', location='company_location',
            description='company_description', employee_count=3
        )
        vacancy = Vacancy.objects.create(
            title='vacancy_title', specialty=specialty,
            company=company, skills='skill_1, skill_2, skill_3',
            description='vacancy_description', salary_min=1,
            salary_max=10
        )

    def test_title_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Название вакансии')

    def test_title_max_length(self):
        vacancy = Vacancy.objects.get(id=1)
        max_length = vacancy._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    def test_specialty_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('specialty').verbose_name
        self.assertEqual(field_label, 'Специальность')

    def test_specialty_related_name(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('specialty').remote_field.related_name
        self.assertEqual(field_label, 'vacancies')

    def test_specialty_relate_model(self):
        vacancy = Vacancy.objects.get(id=1)
        related_model = vacancy._meta.get_field('specialty').remote_field.model.__name__
        self.assertEqual(related_model, 'Specialty')

    def test_company_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('company').verbose_name
        self.assertEqual(field_label, 'Компания')

    def test_company_related_name(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('company').remote_field.related_name
        self.assertEqual(field_label, 'vacancies')

    def test_company_relate_model(self):
        vacancy = Vacancy.objects.get(id=1)
        related_model = vacancy._meta.get_field('company').remote_field.model.__name__
        self.assertEqual(related_model, 'Company')

    def test_skills_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('skills').verbose_name
        self.assertEqual(field_label, 'Навыки')

    def test_skills_max_length(self):
        vacancy = Vacancy.objects.get(id=1)
        max_length = vacancy._meta.get_field('skills').max_length
        self.assertEqual(max_length, 255)

    def test_description_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Текст')

    def test_salary_min_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('salary_min').verbose_name
        self.assertEqual(field_label, 'Зарплата от')

    def test_salary_max_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('salary_max').verbose_name
        self.assertEqual(field_label, 'Зарплата до')

    def test_auto_add(self):
        now = timezone.now()
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=now)):
            vacancy = Vacancy.objects.create(
                title='test', specialty_id=1,
                company_id=1, skills='test',
                salary_min=1, salary_max=2
            )
            self.assertEqual(vacancy.published_at, now)

    def test_object_name(self):
        vacancy = Vacancy.objects.get(id=1)
        expected_object_name = vacancy.title
        self.assertEqual(expected_object_name, str(vacancy))


class CompanyModelTest(TestCase):
    """Тестирует поля модели Company"""

    @classmethod
    def setUpTestData(cls):
        logo = SimpleUploadedFile(name='test.jpg',
                                  content=open('core/tests/test.jpg', 'rb').read(),
                                  content_type='image/jpeg'
                                  )
        Company.objects.create(
            name='company_name', location='company_location',
            description='company_description', employee_count=10,
            logo=logo
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        img = 'media/company_images/test.jpg'
        os.remove(img)

    def test_name_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Название компании')

    def test_name_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_location_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('location').verbose_name
        self.assertEqual(field_label, 'Город')

    def test_location_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('location').max_length
        self.assertEqual(max_length, 50)

    def test_logo_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('logo').verbose_name
        self.assertEqual(field_label, 'Логотип')

    def test_logo_upload_path(self):
        company = Company.objects.get(id=1)
        path = company.logo.url
        self.assertEqual(path, '/media/company_images/test.jpg')

    def test_logo_default_value(self):
        company = Company.objects.create(
            name='company_name', location='company_location',
            description='company_description', employee_count=10,
        )
        self.assertEqual(company.logo, 'https://place-hold.it/100x60')

    def test_description_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Информация о компании')

    def test_employee_count_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('employee_count').verbose_name
        self.assertEqual(field_label, 'Количество сотрудников')

    def test_employee_count_instance(self):
        company = Company.objects.get(id=1)
        self.assertIsInstance(company.employee_count, int)

    def test_owner_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('owner').verbose_name
        self.assertEqual(field_label, 'Владелец')

    def test_owner_is_null(self):
        company = Company.objects.get(id=1)
        self.assertIsNone(company.owner)

    def test_owner_relate_model(self):
        company = Company.objects.get(id=1)
        related_model = company._meta.get_field('owner').remote_field.model.__name__
        self.assertEqual(related_model, 'User')

    def test_object_name(self):
        company = Company.objects.get(id=1)
        expected_object_name = company.name
        self.assertEqual(expected_object_name, str(company))
