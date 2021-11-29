from django.contrib import admin

from .models import Company, Vacancy, Specialty, Application, Resume

admin.site.register(Vacancy)
admin.site.register(Company)
admin.site.register(Specialty)
admin.site.register(Application)
admin.site.register(Resume)