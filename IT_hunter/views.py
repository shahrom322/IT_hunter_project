from django.db.models import Count
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from IT_hunter.models import Specialty, Company, Vacancy


class MainView(TemplateView):
    template_name = 'IT_hunter/index.html'

    def get_context_data(self, **kwargs):
        specialties = Specialty.objects.all().annotate(vacancy_count=Count('vacancies'))
        companies = Company.objects.all().annotate(vacancy_count=Count('vacancies'))
        return {
                'specialties': specialties,
                'companies': companies
        }


class VacanciesList(TemplateView):
    template_name = 'IT_hunter/vacancies.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancies = Vacancy.objects.select_related('specialty', 'company')
        context['vacancies'] = vacancies
        context['vacancies_count'] = vacancies.count()
        return context


class VacanciesBySpecialties(TemplateView):
    template_name = 'IT_hunter/vacancies.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancies = Vacancy.objects.filter(specialty__code=kwargs['code']).select_related('specialty', 'company')
        context['vacancies'] = vacancies
        context['vacancies_count'] = vacancies.count()
        return context


class VacancyDetail(TemplateView):
    template_name = 'IT_hunter/vacancy.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy'] = get_object_or_404(Vacancy, id=kwargs['id'])
        return context


class CompanyDetail(TemplateView):
    template_name = 'IT_hunter/company.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = get_object_or_404(Company, id=kwargs['id'])
        context['vacancies'] = context['company'].vacancies.select_related('specialty', 'company')
        context['vacancies_count'] = len(context['vacancies'])
        return context


def custom_handler404(request, exception):
    return HttpResponseBadRequest('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
