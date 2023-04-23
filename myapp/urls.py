from django.urls import path
from django.views.generic import TemplateView
from .views import UpdateProfileView, CustomProfileView


urlpatterns = [
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('profile/', CustomProfileView.as_view(template_name='myapp/profile.html'), name='profile'),
    path('profile/update/<slug:slug>/', UpdateProfileView.as_view(), name='update_profile'),
]