from django.urls import path
from .views import \
    UpdateProfileView, ProfileView, AddMenuView, \
    MainPageView, OrderView, PriceSetterAjax

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/<slug:slug>/', UpdateProfileView.as_view(), name='update_profile'),
    path('upload_menu/', AddMenuView.as_view(), name='add_menu'),
    path('make_order/', OrderView.as_view(), name='order'),
    path('set_price/',  PriceSetterAjax.as_view(), name='set_price'),
]
