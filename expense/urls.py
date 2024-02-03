from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('userexpenses.urls')),
    path('authentication/', include('authentication.urls')),
    path('preferences/', include('preference.urls')),
    path('income/', include('income.urls')),
    path('admin/', admin.site.urls),
]