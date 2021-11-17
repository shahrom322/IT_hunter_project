import debug_toolbar
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('IT_hunter.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]
