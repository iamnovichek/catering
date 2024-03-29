from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from .views import CustomLoginView, CustomSignupView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('success_register/', TemplateView.as_view(template_name='userauth/success_signup.html'), name='success'),
    path('signup/', CustomSignupView.as_view(), name='signup'),
]

