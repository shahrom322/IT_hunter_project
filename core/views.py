from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.http import HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from core.forms import SignupForm, LoginForm, ApplicationForm, CompanyForm, VacancyForm, ResumeForm
from core.models import Specialty, Company, Vacancy, Resume


User = get_user_model()


class MainView(TemplateView):
    """Вывод главной страницы."""

    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        specialties = Specialty.objects.all().annotate(vacancy_count=Count('vacancies'))
        companies = Company.objects.all().annotate(vacancy_count=Count('vacancies'))[:8]

        vacancy = Vacancy.objects.first()
        examples_for_search = vacancy.skills.split(', ')[:4]

        return {
                'specialties': specialties,
                'companies': companies,
                'examples': examples_for_search,
        }


class VacanciesList(TemplateView):
    """Вывод страницы со списком всех вакансий."""

    template_name = 'core/vacancies.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancies = Vacancy.objects.select_related('specialty', 'company')
        context['vacancies'] = vacancies
        context['vacancies_count'] = len(vacancies)
        return context


class VacanciesBySpecialties(TemplateView):
    """Вывод страницы со списком вакансий по категориям."""

    template_name = 'core/vacancies.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancies = Vacancy.objects.filter(specialty__code=kwargs['code']).select_related('specialty', 'company')
        context['vacancies'] = vacancies
        context['vacancies_count'] = len(vacancies)
        return context


class VacancyDetail(TemplateView):
    """Вывод страницы с полным описанием вакасии и формой для заполнения отклика."""

    template_name = 'core/vacancy.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy'] = get_object_or_404(
            Vacancy.objects.select_related('company', 'specialty'),
            id=kwargs['id'])
        context['form'] = ApplicationForm()
        return context

    def post(self,  request, pk, *args, **kwargs):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save(request, pk)
            return render(request, 'core/send.html', {})
        return render(request, 'core/vacancy.html', self.get_context_data(id=id))


class CompanyDetail(TemplateView):
    """Вывод страницы описания компании."""
    template_name = 'core/company.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = get_object_or_404(Company, id=kwargs['id'])
        context['vacancies'] = context['company'].vacancies.select_related('specialty', 'company')
        context['vacancies_count'] = len(context['vacancies'])
        return context


class MyCompanyView(TemplateView):
    """Если у пользователя создана компания, выводится форма с описанием компании с возможностью редактировать её.
    Если же таковой нет, выводится предложение создать свою компанию."""

    def get(self, request, *args, **kwargs):
        try:
            form = CompanyForm(instance=request.user.company)
            return render(
                request,
                'core/company-edit.html',
                {
                    'form': form,
                    'logo': request.user.company.logo,
                }
            )
        except Company.DoesNotExist:
            return render(request, 'core/company-create.html')

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/mycompany/')
        return render(request, 'core/company-edit.html', {'form': form})


class CreateCompanyView(TemplateView):
    """Вывод страницы с формой для создания своей компании."""

    template_name = 'core/company-edit.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CompanyForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/mycompany/')
        return render(request, 'core/company-edit.html', {'form': form})


class MyVacanciesView(TemplateView):
    """Вывод страницы со списком вакансий, созданные пользователем."""

    template_name = 'core/vacancy-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.prefetch_related(
            'applications').filter(company=self.request.user.company)
        return context


class MyVacancyView(TemplateView):
    """Вывод страницы вакансии, созданной пользователем, с возможностью редактировать ее."""

    def get(self, request, pk, *args, **kwargs):
        vacancy = Vacancy.objects.get(id=pk)
        applications = vacancy.applications.all()
        form = VacancyForm(instance=vacancy)
        return render(request, 'core/vacancy-edit.html', context={
            'form': form,
            'vacancy': vacancy,
            'applications_count': len(applications),
            'applications': applications,
        })

    def post(self, request, pk, *args, **kwargs):
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save(request, pk)
            return HttpResponseRedirect('/mycompany/vacancies')
        return render(request, 'core/vacancy-edit.html', {'form': form})


class CreateVacancyView(TemplateView):
    """Вывод страницы с формой для создания вакансии."""

    def get(self, request, *args, **kwargs):
        form = VacancyForm()
        return render(request, 'core/vacancy-create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save(request, None)
            return HttpResponseRedirect('/mycompany/vacancies')
        return render(request, 'core/vacancy-create.html', {'form': form})


class MyLoginView(LoginView):
    """Вывод страницы с формой для авторизации на сайте."""

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'core/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            # TODO думаю, что это не безопасно
            if not User.objects.filter(username=username):
                form.add_error('username', 'Такого пользователя не существует')
            else:
                form.add_error('password', 'Неверный пароль')
        return render(request, 'core/login.html', {'form': form})


class MySignupView(TemplateView):
    """Вывод страницы для регистрации на сайте."""

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        return render(request, 'core/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'core/register.html', {'form': form})


class MyResumeView(TemplateView):
    """Если у пользователя есть свое резюме, выводится страница с информацией о резюме и возможностью редактировать ее.
    Иначе выводится страница с предложением создать свое резюме."""

    def get(self, request, *args, **kwargs):
        try:
            form = ResumeForm(instance=request.user.resume)
            return render(request, 'core/resume-edit.html', {'form': form})
        except Resume.DoesNotExist:
            return render(request, 'core/resume-create.html')

    def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/myresume/')
        return render(request, 'core/resume-edit.html', {'form': form})


class CreateResumeView(TemplateView):
    """Вывод страницы с формой для создания своего резюме."""

    template_name = 'core/resume-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResumeForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/myresume/')
        return render(request, 'core/resume-edit.html', {'form': form})


class SearchView(TemplateView):
    """Вывод страницы с поиском по вакансиям."""

    template_name = 'core/search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q')
        vacancies = Vacancy.objects.select_related(
            'specialty', 'company').filter(Q(skills__icontains=search_query) | Q(title__icontains=search_query))
        context['vacancies_count'] = len(vacancies)
        context['vacancies'] = vacancies
        context['examples'] = Vacancy.objects.first().skills.split(', ')[:4]
        return context


class ResumesList(TemplateView):
    """Вывод страницы со списком всех резюме."""

    template_name = 'core/resumes.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        resumes = Resume.objects.exclude(status='Не ищу работу').select_related('user')
        context['resumes'] = resumes
        context['resumes_count'] = len(resumes)
        return context


class ResumeDetail(TemplateView):
    """Вывод страницы с полным описанием резюме."""

    template_name = 'core/resume.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume'] = get_object_or_404(
            Resume.objects.exclude(status='Не ищу работу').select_related('specialty', 'user'),
            id=kwargs['id']
        )
        return context


class CompaniesList(TemplateView):
    """Вывод страницы со списком всех компаний."""

    template_name = 'core/companies.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all().annotate(vacancy_count=Count('vacancies'))
        context['companies'] = companies
        context['companies_count'] = len(companies)
        return context


def custom_handler404(request, exception):
    return HttpResponseBadRequest('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
