from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from core.forms import SignupForm, ApplicationForm, CompanyForm, VacancyForm, ResumeForm
from core.models import Specialty, Company, Vacancy, Resume, Application

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


class VacanciesList(ListView):
    """Вывод страницы со списком всех вакансий."""

    model = Vacancy
    template_name = 'core/vacancies.html'
    queryset = Vacancy.objects.select_related('specialty', 'company')
    context_object_name = 'vacancies'


class VacanciesBySpecialties(ListView):
    """Вывод страницы со списком вакансий по категориям."""

    model = Vacancy
    template_name = 'core/vacancies.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacancy.objects.filter(
            specialty__code=self.kwargs['code']).select_related('specialty', 'company')


class VacancyDetail(LoginRequiredMixin, DetailView, CreateView):
    """Вывод страницы с полным описанием вакансии и формой для заполнения отклика."""

    template_name = 'core/vacancy.html'
    queryset = Vacancy.objects.select_related('company', 'specialty')
    context_object_name = 'vacancy'
    model = Application
    form_class = ApplicationForm
    success_url = reverse_lazy('vacancies')

    def form_valid(self, form):
        form.instance.vacancy = self.get_object()
        form.instance.user = self.request.user
        return super(VacancyDetail, self).form_valid(form)


class CompanyDetail(LoginRequiredMixin, DetailView):
    """Вывод страницы описания компании."""

    template_name = 'core/company.html'
    model = Company
    context_object_name = 'company'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies'] = self.object.vacancies.select_related(
            'specialty', 'company'
        )
        return context


class CreateCompanyRequiredMixin:
    """Пользовательский класс-миксин. Перенаправляет пользователя без компании
    на страницу с предложением создать компанию."""

    def dispatch(self, request, *args, **kwargs):
        try:
            company = request.user.company
            return super().dispatch(request, *args, **kwargs)
        except Company.DoesNotExist:
            return redirect('lets_start')


class MyCompanyStartView(LoginRequiredMixin, TemplateView):
    """Вывод страницы с предложением создать компанию. В том случае, если пользователь
    попал на эту страницу и у него есть своя компания, перенаправляем его на страницу
    с редактированием данных о компании."""

    template_name = 'core/company-create.html'

    def get(self, request, *args, **kwargs):
        try:
            company = request.user.company
            return redirect('my_company')
        except Company.DoesNotExist:
            return render(request, self.template_name)


class MyCompanyCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """Вывод страницы для создания компании пользователя."""

    model = Company
    form_class = CompanyForm
    template_name = 'core/company-edit.html'
    success_url = reverse_lazy('my_company')
    success_message = 'Компания создана.'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(MyCompanyCreateView, self).form_valid(form)


class MyCompanyView(
    LoginRequiredMixin,
    CreateCompanyRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    """Вывод страницы с данными о компании пользователя и возможностью редактировать ее."""

    template_name = 'core/company-edit.html'
    model = Company
    form_class = CompanyForm
    success_message = 'Данные обновлены.'

    def get_object(self, queryset=None):
        return self.request.user.company

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = self.object.logo
        return context


class MyVacanciesView(LoginRequiredMixin, CreateCompanyRequiredMixin, ListView):
    """Вывод страницы со списком вакансий, созданные пользователем."""

    template_name = 'core/vacancy-list.html'
    model = Vacancy
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacancy.objects.prefetch_related(
                'applications').filter(company=self.request.user.company)


class MyVacancyView(LoginRequiredMixin, CreateCompanyRequiredMixin, UpdateView):

    model = Vacancy
    template_name = 'core/vacancy-edit.html'
    form_class = VacancyForm
    context_object_name = 'vacancy'

    def get_object(self, queryset=None):
        return get_object_or_404(
                    Vacancy.objects.prefetch_related('applications'),
                    company=self.request.user.company, pk=self.kwargs['pk']
                )

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = self.object.applications.all()
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(MyVacancyView, self).form_valid(form)


class CreateVacancyView(
    LoginRequiredMixin,
    CreateCompanyRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """Вывод страницы с формой для создания вакансии."""

    model = Vacancy
    form_class = VacancyForm
    template_name = 'core/vacancy-create.html'
    success_url = reverse_lazy('my_vacancies')
    success_message = 'Вакансия создана.'

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super(CreateVacancyView, self).form_valid(form)


class MySignupView(SuccessMessageMixin, CreateView):
    """Вывод страницы для регистрации на сайте."""

    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    form_class = SignupForm
    success_message = 'Аккаунт создан.'


class CreateResumeRequiredMixin:
    """Пользовательский класс-миксин. Перенаправляет пользователя без резюме
    на страницу с предложением создать резюме."""

    def dispatch(self, request, *args, **kwargs):
        try:
            resume = request.user.resume
            return super().dispatch(request, *args, **kwargs)
        except Resume.DoesNotExist:
            return redirect('lets_start_resume')


class MyResumeStartView(LoginRequiredMixin, TemplateView):
    """Вывод страницы с предложением создать резюме. В том случае, если пользователь
    попал на эту страницу и у него есть свое резюме, перенаправляем его на страницу
    с редактированием данных о резюме."""

    template_name = 'core/resume-create.html'

    def get(self, request, *args, **kwargs):
        try:
            resume = request.user.resume
            return redirect('my_resume')
        except Resume.DoesNotExist:
            return render(request, self.template_name)


class MyResumeView(
    LoginRequiredMixin,
    CreateResumeRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    """Вывод страницы с данными о резюме пользователя и возможностью редактировать ее."""

    model = Resume
    template_name = 'core/resume-edit.html'
    form_class = ResumeForm
    context_object_name = 'resume'
    success_message = 'Данные обновлены.'

    def get_object(self, queryset=None):
        return Resume.objects.select_related('user', 'specialty').get(
                    user=self.request.user
                )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo'] = self.object.photo
        return context

    def get_success_url(self):
        return self.request.path


class CreateResumeView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """Вывод страницы для создания резюме пользователя."""

    model = Resume
    form_class = ResumeForm
    template_name = 'core/resume-edit.html'
    success_url = reverse_lazy('my_resume')
    success_message = 'Резюме создано.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateResumeView, self).form_valid(form)


class SearchView(ListView):
    """Вывод страницы с поиском по вакансиям."""

    model = Vacancy
    template_name = 'core/search.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        search_query = self.request.GET.get('q')
        if search_query:
            vacancies = Vacancy.objects.select_related(
                'specialty', 'company'
            ).filter(Q(skills__icontains=search_query) | Q(title__icontains=search_query))
        else:
            vacancies = Vacancy.objects.select_related(
                'specialty', 'company'
            ).all()
        return vacancies

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['examples'] = Vacancy.objects.first().skills.split(', ')[:4]
        return context


class ResumesList(LoginRequiredMixin, ListView):
    """Вывод страницы со списком всех резюме."""

    model = Resume
    queryset = Resume.objects.exclude(status='Не ищу работу').select_related('user')
    context_object_name = 'resumes'
    template_name = 'core/resumes.html'


class ResumeDetail(LoginRequiredMixin, DetailView):
    """Вывод страницы с полным описанием резюме."""

    model = Resume
    template_name = 'core/resume.html'
    context_object_name = 'resume'


class CompaniesList(LoginRequiredMixin, ListView):
    """Вывод страницы со списком всех компаний."""

    model = Company
    template_name = 'core/companies.html'
    context_object_name = 'companies'


def custom_handler404(request, exception):
    return HttpResponseBadRequest('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
