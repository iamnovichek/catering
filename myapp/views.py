from pprint import pprint
from django.forms import formset_factory, BaseFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.views.generic import UpdateView
from .forms import ProfileUpdateForm, AddMenuForm, OrderForm
from django.http import JsonResponse
from .models import Menu, Order


class CustomTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'myapp/order.html'


class MainPageView(CreateView):
    template_name = 'myapp/home.html'
    menu = {
        "first_courses": list(Menu.objects.values_list('first_course', flat=True)),
        "second_courses": list(Menu.objects.values_list('second_course', flat=True)),
        "desserts": list(Menu.objects.values_list('dessert', flat=True)),
        "drinks": list(Menu.objects.values_list('drink', flat=True))
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'menu': self.menu})


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


class CustomBaseFormSet(BaseFormSet):

    def is_valid(self):
        res = super(CustomBaseFormSet, self).is_valid()
        if not res:
            pprint(self.errors)
            return res

        return res


class OrderView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "myapp/order.html"
    success_url = reverse_lazy("order_success")
    model = Order
    formset_class = formset_factory(form=OrderForm, formset=CustomBaseFormSet, extra=5)

    def get_form_kwargs(self):
        kwargs = super(OrderView, self).get_form_kwargs()
        kwargs['form_kwargs'] = {"user": self.request.user}
        return kwargs

    def get(self, request, *args, **kwargs):
        days = self._get_days()
        for day in days:
            try:
                if Order.objects.get(date=day, user_id=request.user).user_id:
                    return redirect('order_error')
            except:
                break

        formset = self.formset_class()

        return render(request, self.template_name, {
            'formset': formset,
            'Monday': days[0],
            'Tuesday': days[1],
            'Wednesday': days[2],
            'Thursday': days[3],
            'Friday': days[4]
        })

    def post(self, request, *args, **kwargs):
        formset = self.formset_class(request.POST or None, form_kwargs={'user': request.user})
        if formset.is_valid():
            for form in formset:
                form.save()

            return redirect(self.success_url)

        return redirect('order')

    def _get_days(self):
        from datetime import date, timedelta

        today = date.today()
        current_weekday = today.weekday()
        start_of_week = today + timedelta(days=7 - current_weekday)
        return [(start_of_week + timedelta(days=i)) for i in range(5)]


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

        return JsonResponse({'response': menu_data})


class TotalAmountCounterAjax(View):
    total_money = 30

    def post(self, request, *args, **kwargs):
        fc_quantity = self._get_value('fc_quantity')
        fc_price = self._get_value('fc_price')
        sc_quantity = self._get_value('sc_quantity')
        sc_price = self._get_value('sc_price')
        des_quantity = self._get_value('des_quantity')
        des_price = self._get_value('des_price')
        dr_quantity = self._get_value('dr_quantity')
        dr_price = self._get_value('dr_price')
        result = self.total_money - (
                fc_price * fc_quantity +
                sc_price * sc_quantity +
                des_price * des_quantity +
                dr_price * dr_quantity
        )

        return JsonResponse({'response': result,
                             'deducted_amount': result < 0})

    def _get_value(self, field_name: str):
        try:
            return float(self.request.POST.get(f'{field_name}'))
        except:
            return 0


class HistoryView(CreateView):
    template_name = "myapp/history.html"

    def get(self, request, *args, **kwargs):
        days = self._get_days()
        return render(request, self.template_name, {

        })

    def _get_days(self):
        from datetime import date, timedelta

        today = date.today()
        current_weekday = today.weekday()
        start_of_week = today + timedelta(days=7 - current_weekday)
        return [(start_of_week + timedelta(days=i)) for i in range(5)]

