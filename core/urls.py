from django.contrib.auth.views import LogoutView
from django.urls import path

from core import views
from config import settings

handler404 = views.custom_handler404
handler500 = views.custom_handler500

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('search/', views.SearchView.as_view(), name='search'),

    path('vacancies/', views.VacanciesList.as_view(), name='vacancies'),
    path('vacancies/cat/<str:code>', views.VacanciesBySpecialties.as_view(), name='vacancies_by_specialties'),
    path('vacancies/<int:id>', views.VacancyDetail.as_view(), name='vacancy_detail'),

    path('companies/', views.CompaniesList.as_view(), name='companies'),
    path('companies/<int:id>', views.CompanyDetail.as_view(), name='company_detail'),

    path('resumes/', views.ResumesList.as_view(), name='resumes'),
    path('resumes/<int:id>', views.ResumeDetail.as_view(), name='resume_detail'),

    path('mycompany/', views.MyCompanyView.as_view(), name='my_company'),
    path('mycompany/letsstart', views.MyCompanyView.as_view(), name='lets_start'),
    path('mycompany/create', views.CreateCompanyView.as_view(), name='create_company'),

    path('mycompany/vacancies', views.MyVacanciesView.as_view(), name='my_vacancies'),
    path('mycompany/vacancies/<int:id>', views.MyVacancyView.as_view(), name='my_vacancy'),
    path('mycompany/vacancies/create', views.CreateVacancyView.as_view(), name='create_vacancy'),

    path('myresume/', views.MyResumeView.as_view(), name='my_resume'),
    path('myresume/letsstart', views.MyResumeView.as_view(), name='lets_start_resume'),
    path('myresume/create', views.CreateResumeView.as_view(), name='create_resume'),

    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('register/', views.MySignupView.as_view(),  name='register'),
]
