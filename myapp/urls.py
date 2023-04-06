from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('profile/', TemplateView.as_view(template_name='myapp/profile.html'), name='profile')
]