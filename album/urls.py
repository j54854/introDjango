from django.urls import path
from . import views

app_name = 'album'

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('showall/', views.showall, name='showall'),
]
