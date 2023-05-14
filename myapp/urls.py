from django.urls import path
from .views import UpdateProfileView, ProfileView, AddMenuView, MainPageView

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(template_name='myapp/profile.html'), name='profile'),
    path('profile/update/<slug:slug>/', UpdateProfileView.as_view(), name='update_profile'),
    path('upload_menu/', AddMenuView.as_view(), name='add_menu'),
]
