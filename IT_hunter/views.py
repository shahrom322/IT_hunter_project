from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.http import HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from IT_hunter.forms import SignupForm, LoginForm, ApplicationForm, CompanyForm, VacancyForm, ResumeForm
from IT_hunter.models import Specialty, Company, Vacancy


class MainView(TemplateView):
    template_name = 'IT_hunter/index.html'

    def get_context_data(self, **kwargs):
        specialties = Specialty.objects.all().annotate(vacancy_count=Count('vacancies'))
        companies = Company.objects.all().annotate(vacancy_count=Count('vacancies'))[:8]
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
        context['vacancies_count'] = len(vacancies)
        return context


class VacanciesBySpecialties(TemplateView):
    template_name = 'IT_hunter/vacancies.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancies = Vacancy.objects.filter(specialty__code=kwargs['code']).select_related('specialty', 'company')
        context['vacancies'] = vacancies
        context['vacancies_count'] = len(vacancies)
        return context


class VacancyDetail(TemplateView):
    template_name = 'IT_hunter/vacancy.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy'] = get_object_or_404(Vacancy.objects.select_related('company', 'specialty'), id=kwargs['id'])
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


class MyCompanyView(TemplateView):

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
    template_name = 'IT_hunter/company-edit.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CompanyForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/mycompany/')
        return render(request, 'IT_hunter/company-edit.html', {'form': form})


class MyVacanciesView(TemplateView):
    template_name = 'IT_hunter/vacancy-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO оптимизировать запрос .prefetch_related('applications')
        context['vacancies'] = Vacancy.objects.prefetch_related(
            'applications').filter(company=self.request.user.company)
        return context


class MyVacancyView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        vacancy = Vacancy.objects.get(id=id)
        applications = vacancy.applications.all()
        form = VacancyForm(instance=vacancy)
        return render(request, 'IT_hunter/vacancy-edit.html', context={
            'form': form,
            'vacancy': vacancy,
            'applications_count': len(applications),
            'applications': applications,
        })

    def post(self, request, id, *args, **kwargs):
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save(request, id)
            return HttpResponseRedirect('/mycompany/vacancies')
        return render(request, 'IT_hunter/vacancy-edit.html', {'form': form})


class CreateVacancyView(TemplateView):

    def get(self, request, *args, **kwargs):
        form = VacancyForm()
        return render(request, 'IT_hunter/vacancy-create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save(request, None)
            return HttpResponseRedirect('/mycompany/vacancies')
        return render(request, 'IT_hunter/vacancy-create.html', {'form': form})


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


class MyResumeView(TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            form = ResumeForm(instance=request.user.resume)
            return render(request, 'IT_hunter/resume-edit.html', {'form': form})
        except ObjectDoesNotExist:
            return render(request, 'IT_hunter/resume-create.html')

    def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/myresume/')
        return render(request, 'IT_hunter/resume-edit.html', {'form': form})


class CreateResumeView(TemplateView):
    template_name = 'IT_hunter/resume-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResumeForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/myresume/')
        return render(request, 'IT_hunter/resume-edit.html', {'form': form})


class SearchView(TemplateView):
    template_name = 'IT_hunter/search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search')
        vacancies = Vacancy.objects.select_related(
            'specialty', 'company').filter(Q(skills__icontains=search_query)|Q(title__icontains=search_query))
        context['vacancies'] = vacancies
        context['vacancies_count'] = len(vacancies)
        return context


def custom_handler404(request, exception):
    return HttpResponseBadRequest('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
