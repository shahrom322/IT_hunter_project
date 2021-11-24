from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from IT_hunter.forms import SignupForm, LoginForm, ApplicationForm, CompanyForm
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
        context['form'] = ApplicationForm()
        return context

    def post(self,  request, id, *args, **kwargs):
        form = ApplicationForm(request.POST)
        print(form)
        if form.is_valid():
            # TODO make validation
            form.save(request, id)
            return render(request, 'IT_hunter/send.html', {})
        else:
            return render(
                request,
                'IT_hunter/vacancy.html',
                self.get_context_data(id=id)
            )


class CompanyDetail(TemplateView):
    template_name = 'IT_hunter/company.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = get_object_or_404(Company, id=kwargs['id'])
        context['vacancies'] = context['company'].vacancies.select_related('specialty', 'company')
        context['vacancies_count'] = len(context['vacancies'])
        return context


class SendVacancyView(TemplateView):
    template_name = 'IT_hunter/send.html'


class MyCompanyView(TemplateView):
    template_name = 'IT_hunter/company-edit.html'

    def get(self, request, *args, **kwargs):
        try:
            form = CompanyForm(instance=request.user.company)
            return render(
                request,
                'IT_hunter/company-edit.html',
                {
                    'form': form,
                    'logo': request.user.company.logo,
                }
            )
        except ObjectDoesNotExist:
            return render(request, 'IT_hunter/company-create.html')

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/mycompany/')
        return render(request, 'IT_hunter/company-edit.html', {'form': form})


class CreateCompanyView(TemplateView):
    # TODO протестировать создание компании, вывод лого

    template_name = 'IT_hunter/company-edit.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CompanyForm()
        return context


class MyVacanciesView(TemplateView):
    template_name = ''


class MyVacancyView(TemplateView):
    template_name = ''


class MyLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'IT_hunter/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            # TODO make validation
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'IT_hunter/login.html', {'form': form})


class MySignupView(TemplateView):

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        return render(request, 'IT_hunter/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'IT_hunter/register.html', {'form': form})


def custom_handler404(request, exception):
    return HttpResponseBadRequest('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
