from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse

from core.forms import ApplicationForm
from core.management.commands import db_dump, makesuperuser
from core.models import Vacancy


class ViewsTest(TestCase):
    """Тестирование контроллеров сайта."""

    @classmethod
    def setUpTestData(cls):
        populate_database_command = db_dump.Command()
        populate_database_command.handle()
        super_user_command = makesuperuser.Command()
        super_user_command.handle()

    def test_main_view(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['specialties'])
        self.assertEqual(len(response.context['companies']), 8)
        self.assertIsNot(response.context['examples'], '')
        self.assertIsInstance(response.context['examples'], list)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_search_view(self):
        response = self.client.get(reverse('search'), {'q': 'Python'})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['vacancies'])
        self.assertIsInstance(response.context['vacancies'], QuerySet)

    def test_vacancies_list_view(self):
        response = self.client.get(reverse('vacancies'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['vacancies'], QuerySet)
        self.assertTemplateUsed(response, 'core/vacancies.html')

    def test_vacancies_by_specialty_view(self):
        response = self.client.get(reverse('vacancies_by_specialties', kwargs={'code': 'backend'}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['vacancies'], QuerySet)
        self.assertEqual(len(response.context['vacancies']), 5)
        self.assertTemplateUsed(response, 'core/vacancies.html')

    def test_vacancy_detail_view(self):
        non_authenticated_response = self.client.get(
            reverse('vacancy_detail', kwargs={'pk': 1})
        )
        self.assertEqual(non_authenticated_response.status_code, 302)
        self.assertRedirects(
            non_authenticated_response,
            '/login?next=/vacancies/1',
            target_status_code=301
        )

        self.client.login(username='admin', password='admin')
        authenticated_response = self.client.get(
            reverse('vacancy_detail', kwargs={'pk': 1})
        )
        self.assertEqual(authenticated_response.status_code, 200)
        self.assertTemplateUsed(authenticated_response, 'core/vacancy.html')
        self.assertIsInstance(authenticated_response.context['vacancy'], Vacancy)
        self.assertIsInstance(authenticated_response.context['form'], ApplicationForm)
