from django.contrib.auth.views import LogoutView
from django.urls import path

from IT_hunter.views import custom_handler500, custom_handler404, MainView, VacanciesList, VacancyDetail, \
    VacanciesBySpecialties, CompanyDetail, MyCompanyView, MyVacanciesView, MyVacancyView, MyLoginView, \
    CreateCompanyView, MySignupView, CreateVacancyView, CreateResumeView, MyResumeView, SearchView

from config import settings

handler404 = custom_handler404
handler500 = custom_handler500
urlpatterns = [
    path('', MainView.as_view(), name='main'),
    # TODO regex search view
    path('search', SearchView.as_view(), name='search'),

    path('vacancies/', VacanciesList.as_view(), name='vacancies'),
    path('vacancies/cat/<str:code>', VacanciesBySpecialties.as_view(), name='vacancies_by_specialties'),
    path('vacancies/<int:id>', VacancyDetail.as_view(), name='vacancy_detail'),
    path('companies/<int:id>', CompanyDetail.as_view(), name='company_detail'),

    path('mycompany/', MyCompanyView.as_view(), name='my_company'),
    path('mycompany/letsstart', MyCompanyView.as_view(), name='lets_start'),
    path('mycompany/create', CreateCompanyView.as_view(), name='create_company'),

    path('mycompany/vacancies', MyVacanciesView.as_view(), name='my_vacancies'),
    path('mycompany/vacancies/<int:id>', MyVacancyView.as_view(), name='my_vacancy'),
    path('mycompany/vacancies/create', CreateVacancyView.as_view(), name='create_vacancy'),

    path('myresume/', MyResumeView.as_view(), name='my_resume'),
    path('myresume/letsstart', MyResumeView.as_view(), name='lets_start_resume'),
    path('myresume/create', CreateResumeView.as_view(), name='create_resume'),

    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('register/', MySignupView.as_view(),  name='register'),
]

