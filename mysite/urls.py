from django.contrib import admin
from django.urls import include, path
from django.views.generic import base
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('album/', include('album.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', base.RedirectView.as_view(pattern_name="polls:login")),
    path('accounts/profile/', base.RedirectView.as_view(pattern_name="polls:index")),
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
