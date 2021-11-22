from django.urls import path

from IT_hunter.views import custom_handler500, custom_handler404, MainView, VacanciesList, VacancyDetail, \
    VacanciesBySpecialties, CompanyDetail

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('vacancies/', VacanciesList.as_view(), name='vacancies'),
    path('vacancies/cat/<str:code>', VacanciesBySpecialties.as_view(), name='vacancies_by_specialties'),
    path('vacancies/<int:id>', VacancyDetail.as_view(), name='vacancy_detail'),
    path('companies/<int:id>', CompanyDetail.as_view(), name='company_detail'),
]
