from django.urls import path
from django.views.generic import TemplateView
from .views import \
    UpdateProfileView, ProfileView, AddMenuView, \
    MainPageView, OrderView, TotalAmountCounterAjax, \
    CustomTemplateView, PriceSetterAjax, HistoryView, \
    HistoryDefaultSetterAjax, HistoryAnotherWeekSetterAjax

app_name = 'myapp'

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
    path('history/', HistoryView.as_view(), name='history'),
    path('history-set-price/', HistoryDefaultSetterAjax.as_view(), name='history_set_price'),
    path('history-another-week/', HistoryAnotherWeekSetterAjax.as_view(), name='history-another-week'),
    path('order-access-denied/', CustomTemplateView.as_view(template_name='myapp/access_denied_order.html'
                                                            ), name='weekend')
]
