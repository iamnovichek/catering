from django.urls import path
from django.views.generic import TemplateView
from .views import \
    UpdateProfileView, ProfileView, AddMenuView, \
    MainPageView, OrderView, TotalAmountCounterAjax, CustomTemplateView, PriceSetterAjax

urlpatterns = [
    path('', TemplateView.as_view(template_name='myapp/welcome.html'), name='welcome'),
    path('smakolyk/', MainPageView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/<slug:slug>/', UpdateProfileView.as_view(), name='update_profile'),
    path('upload_menu/', AddMenuView.as_view(), name='add_menu'),
    path('make_order/', OrderView.as_view(), name='order'),
    path('order-error/', CustomTemplateView.as_view(template_name='myapp/order_error.html'), name='order_error'),
    path('success-order/', CustomTemplateView.as_view(template_name='myapp/order_success.html'), name='order_success'),
    path('set_price/', PriceSetterAjax.as_view(), name='set_price'),
    path('set_total_price/', TotalAmountCounterAjax.as_view(), name='set_total_price'),
    path('history/', CustomTemplateView.as_view(template_name="myapp/history.html"), name='history'),
]
