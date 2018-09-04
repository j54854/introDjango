from django.contrib import admin
from django.urls import include, path
from django.views.generic import base

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', base.RedirectView.as_view(pattern_name="polls:login")),
    path('accounts/profile/', base.RedirectView.as_view(pattern_name="polls:index")),
]
