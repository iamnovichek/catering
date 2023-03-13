from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('logout/', LogoutView.as_view(), name='logout')
]