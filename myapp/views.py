from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.views.generic import UpdateView
from .forms import ProfileUpdateForm, OrderForm, AddMenuForm, MainPageForm
from django.forms import formset_factory
from django.http import JsonResponse
from .models import Menu


class CustomTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'myapp/order.html'


class MainPageView(CreateView):
    template_name = 'myapp/home.html'
    form_class = MainPageForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class AddMenuView(LoginRequiredMixin, CreateView):
    form_class = AddMenuForm
    login_url = '/admin/login/'
    success_url = reverse_lazy('admin:myapp_menu_changelist')
    template_name = 'admin/upload_menu.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect(self.success_url)

        return redirect(reverse_lazy('add_menu'))


class ProfileView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = 'myapp/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    login_url = reverse_lazy('login')
    template_name = "myapp/update_profile.html"
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.userprofile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,
                               request.FILES,
                               instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        
        return render(request, self.template_name, {'form': form})


class OrderView(CreateView):
    form_class = OrderForm
    template_name = "myapp/order.html"
    success_url = reverse_lazy("order_success")

    def get(self, request, *args, **kwargs):
        days = self._get_days()
        form1 = self.form_class()
        form2 = self.form_class()
        form3 = self.form_class()
        form4 = self.form_class()
        form5 = self.form_class()
        return render(request, self.template_name, {
            'form1': form1,
            'form2': form2,
            'form3': form3,
            'form4': form4,
            'form5': form5,
            'Monday': days[0],
            'Tuesday': days[1],
            'Wednesday': days[2],
            'Thursday': days[3],
            'Friday': days[4]
        })

    def _get_days(self):
        from datetime import date, timedelta

        today = date.today()
        current_weekday = today.weekday()
        start_of_week = today - timedelta(days=current_weekday)
        return [(start_of_week + timedelta(days=i)).day for i in range(5)]


class PriceSetterAjax(View):
    def get(self, request, *args, **kwargs):
        menu_data = {
            'first_courses': list(Menu.objects.values_list('first_course', flat=True)),
            'first_course_prices': list(Menu.objects.values_list('first_course_price', flat=True)),
            'second_courses': list(Menu.objects.values_list('second_course', flat=True)),
            'second_course_prices': list(Menu.objects.values_list('second_course_price', flat=True)),
            'desserts': list(Menu.objects.values_list('dessert', flat=True)),
            'dessert_prices': list(Menu.objects.values_list('dessert_price', flat=True)),
            'drinks': list(Menu.objects.values_list('drink', flat=True)),
            'drinks_prices': list(Menu.objects.values_list('drink_price', flat=True)),
        }

        test_response = "1"

        return JsonResponse(list(test_response))

