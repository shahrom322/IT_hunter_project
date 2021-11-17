from django.http import HttpResponse
from django.urls import path

from IT_hunter.views import test

urlpatterns = [
    path('', test),
]