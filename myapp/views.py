from datetime import datetime, time, timedelta, date
from django.forms import formset_factory, BaseFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.views.generic import UpdateView
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from userauth.models import CustomUser
from .forms import ProfileUpdateForm, AddMenuForm, OrderForm
from .models import Menu, Order, History
from .tasks import upload_menu_task


class CustomTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')


class MainPageView(CreateView):
    template_name = 'myapp/home.html'

    def get(self, request, *args, **kwargs):
        menu = {
            "first_courses": list(Menu.objects.values_list('first_course', flat=True)),
            "second_courses": list(Menu.objects.values_list('second_course', flat=True)),
            "desserts": list(Menu.objects.values_list('dessert', flat=True)),
            "drinks": list(Menu.objects.values_list('drink', flat=True)),
            "len": len(list(Menu.objects.values_list('first_course', flat=True))),
            "range": range(len(list(Menu.objects.values_list('first_course', flat=True)))),
        }
        return render(request, self.template_name, {
            'menu': menu,
            'has_order': request.user.id in list(History.objects.values_list('user_id', flat=True))
        })


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
            try:
                res = form.parse_file()
            except:
                messages.error(request, "Ivalid file! try again!")
                return redirect(reverse_lazy('myapp:add_menu'))
            upload_menu_task.apply_async(args=[res], countdown=self.get_countdown_time())
            return redirect(self.success_url)

        return redirect(reverse_lazy('myapp:add_menu'))

    @classmethod
    def get_countdown_time(cls):
        if datetime.now().weekday() >= 4:
            if datetime.now().weekday() > 4:
                return 0
            if datetime.now().weekday() == 4 and datetime.now().time().hour >= 18:
                return 0
            if datetime.now().weekday() == 4 and datetime.now().time().hour < 18:
                return cls.get_seconds()

            return cls.get_seconds()

    @staticmethod
    def get_seconds():
        now = datetime.now()
        friday_deadline = datetime.combine(now.date(), time(18, 0)) + timedelta(
            days=(4 - now.weekday()) % 7)
        time_difference = friday_deadline - now
        seconds_left = time_difference.total_seconds()
        final_time = int(seconds_left)
        return final_time


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
    success_url = reverse_lazy('myapp:profile')

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
    renderer = None
    absolute_max = 1000
    min_num = 0
    form = OrderForm
    can_order = True
    can_delete = True
    can_delete_extra = True
    validate_max = 1000
    validate_min = 0
    max_num = 1000

    def is_valid(self):
        res = super().is_valid()
        if not res:
            print(self.errors)
            return res
        return res


class OrderView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "myapp/order.html"
    success_url = reverse_lazy("myapp:order_success")
    model = Order
    formset_class = formset_factory(form=OrderForm, formset=CustomBaseFormSet, extra=5)

    def get_form_kwargs(self):
        kwargs = super(OrderView, self).get_form_kwargs()
        kwargs['form_kwargs'] = {"user": self.request.user}
        return kwargs

    def get(self, request, *args, **kwargs):

        if datetime.now().weekday() > 4 or (datetime.now().weekday() >= 4 and
                                            datetime.now().time().hour >= 18):
            return redirect('myapp:weekend')

        days = self._get_days()
        for day in days:
            try:
                if Order.objects.get(date=day, user_id=request.user.id):
                    return redirect('myapp:order_error')
            except Order.DoesNotExist:
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
        formset = self.formset_class(request.POST, form_kwargs={'user': request.user})

        if formset.is_valid():
            for form in formset:
                order = form.save()
                data = self._get_data(order)
                result = self.get_sum(data)

                if result > 200:
                    cur_user = CustomUser.objects.get(id=request.user.id)
                    oversum = result - 200
                    send_mail(
                        subject="Oversum",
                        message=f'''{cur_user.userprofile.first_name} {cur_user.userprofile.last_name}
                        -> {oversum} ₴ oversum.''',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[settings.ACCOUNTANT],
                        fail_silently=False
                    )

                    send_mail(
                        subject="Oversum",
                        message=f'''Dear {cur_user.userprofile.first_name} {cur_user.userprofile.last_name},
                                    you did {oversum} oversum for {order.date}. The difference will be
                                    deducted from your salary.''',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[cur_user],
                        fail_silently=False
                    )

            return redirect(self.success_url)

        return redirect('myapp:order')

    @staticmethod
    def _get_days():
        today = date.today()
        current_weekday = today.weekday()
        start_of_week = today + timedelta(days=7 - current_weekday)
        return [(start_of_week + timedelta(days=i)) for i in range(5)]

    @staticmethod
    def get_price(dish_val, dish_type):
        print(list(Menu.objects.values_list(f"{dish_type}", flat=True)))
        if dish_val in list(Menu.objects.values_list(f"{dish_type}", flat=True)):
            idx = list(Menu.objects.values_list(f"{dish_type}", flat=True)).index(dish_val)
            return list(Menu.objects.values_list(f"{dish_type}_price", flat=True))[idx]
        return 0

    def _get_data(self, order):
        return {
            "fc_quantity": order.first_course_quantity,
            "fc_price": self.get_price(order.first_course, 'first_course'),
            "sc_quantity": order.second_course_quantity,
            "sc_price": self.get_price(order.second_course, 'second_course'),
            "des_quantity": order.dessert_quantity,
            "des_price": self.get_price(order.dessert, 'dessert'),
            "dr_quantity": order.drink_quantity,
            "dr_price": self.get_price(order.drink, 'drink')
        }

    @staticmethod
    def get_sum(data):
        res = (data['fc_quantity'] * data['fc_price'] +
               data['sc_quantity'] * data['sc_price'] +
               data['des_quantity'] * data['des_price'] +
               data['dr_quantity'] * data['dr_price']
               )
        return res


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
    total_money = 200

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
        days = self._get_cur_days()
        try:
            data = {
                'monday': History.objects.get(date=days[0], user_id=request.user.id),
                'tuesday': History.objects.get(date=days[1], user_id=request.user.id),
                'wednesday': History.objects.get(date=days[2], user_id=request.user.id),
                'thursday': History.objects.get(date=days[3], user_id=request.user.id),
                'friday': History.objects.get(date=days[4], user_id=request.user.id)
            }
            return render(request, self.template_name, {'data': data})
        except:
            days = self._get_next_days()
            data = {
                'monday': History.objects.get(date=days[0], user_id=request.user),
                'tuesday': History.objects.get(date=days[1], user_id=request.user),
                'wednesday': History.objects.get(date=days[2], user_id=request.user),
                'thursday': History.objects.get(date=days[3], user_id=request.user),
                'friday': History.objects.get(date=days[4], user_id=request.user)
            }
            return render(request, self.template_name, {'data': data})

    @staticmethod
    def _get_cur_days():
        from datetime import date, timedelta

        today = date.today()
        current_weekday = today.weekday()
        start_of_week = today + timedelta(days=0 - current_weekday)
        return [(start_of_week + timedelta(days=i)) for i in range(5)]

    @staticmethod
    def _get_next_days():
        from datetime import date, timedelta

        today = date.today()
        current_weekday = today.weekday()
        start_of_week = today + timedelta(days=7 - current_weekday)
        return [(start_of_week + timedelta(days=i)) for i in range(5)]


class HistoryDefaultSetterAjax(View):

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

        return JsonResponse({'data': menu_data})


class HistoryAnotherWeekSetterAjax(View):
    def get(self, request, *args, **kwargs):

        chosen_date = request.GET.get("date")
        if chosen_date not in [str(date) for date in list(History.objects.values_list('date', flat=True))]:
            return JsonResponse({"date_exists": False})

        days = self._get_dates_in_week(chosen_date)

        data = {
            'monday': {
                'first_course': History.objects.get(date=days[0], user_id=request.user).first_course,
                'first_course_quantity': History.objects.get(date=days[0], user_id=request.user).first_course_quantity,
                'second_course': History.objects.get(date=days[0], user_id=request.user).second_course,
                'second_course_quantity': History.objects.get(date=days[0],
                                                              user_id=request.user).second_course_quantity,
                'dessert': History.objects.get(date=days[0], user_id=request.user).dessert,
                'dessert_quantity': History.objects.get(date=days[0], user_id=request.user).dessert_quantity,
                'drink': History.objects.get(date=days[0], user_id=request.user).drink,
                'drink_quantity': History.objects.get(date=days[0], user_id=request.user).drink_quantity
            },
            'tuesday': {
                'first_course': History.objects.get(date=days[1], user_id=request.user).first_course,
                'first_course_quantity': History.objects.get(date=days[1], user_id=request.user).first_course_quantity,
                'second_course': History.objects.get(date=days[1], user_id=request.user).second_course,
                'second_course_quantity': History.objects.get(date=days[1],
                                                              user_id=request.user).second_course_quantity,
                'dessert': History.objects.get(date=days[1], user_id=request.user).dessert,
                'dessert_quantity': History.objects.get(date=days[1], user_id=request.user).dessert_quantity,
                'drink': History.objects.get(date=days[1], user_id=request.user).drink,
                'drink_quantity': History.objects.get(date=days[1], user_id=request.user).drink_quantity
            },
            'wednesday': {
                'first_course': History.objects.get(date=days[2], user_id=request.user).first_course,
                'first_course_quantity': History.objects.get(date=days[2], user_id=request.user).first_course_quantity,
                'second_course': History.objects.get(date=days[2], user_id=request.user).second_course,
                'second_course_quantity': History.objects.get(date=days[2],
                                                              user_id=request.user).second_course_quantity,
                'dessert': History.objects.get(date=days[2], user_id=request.user).dessert,
                'dessert_quantity': History.objects.get(date=days[2], user_id=request.user).dessert_quantity,
                'drink': History.objects.get(date=days[2], user_id=request.user).drink,
                'drink_quantity': History.objects.get(date=days[2], user_id=request.user).drink_quantity
            },
            'thursday': {
                'first_course': History.objects.get(date=days[3], user_id=request.user).first_course,
                'first_course_quantity': History.objects.get(date=days[3], user_id=request.user).first_course_quantity,
                'second_course': History.objects.get(date=days[3], user_id=request.user).second_course,
                'second_course_quantity': History.objects.get(date=days[3],
                                                              user_id=request.user).second_course_quantity,
                'dessert': History.objects.get(date=days[3], user_id=request.user).dessert,
                'dessert_quantity': History.objects.get(date=days[3], user_id=request.user).dessert_quantity,
                'drink': History.objects.get(date=days[3], user_id=request.user).drink,
                'drink_quantity': History.objects.get(date=days[3], user_id=request.user).drink_quantity
            },
            'friday': {
                'first_course': History.objects.get(date=days[4], user_id=request.user).first_course,
                'first_course_quantity': History.objects.get(date=days[4], user_id=request.user).first_course_quantity,
                'second_course': History.objects.get(date=days[4], user_id=request.user).second_course,
                'second_course_quantity': History.objects.get(date=days[4],
                                                              user_id=request.user).second_course_quantity,
                'dessert': History.objects.get(date=days[4], user_id=request.user).dessert,
                'dessert_quantity': History.objects.get(date=days[4], user_id=request.user).dessert_quantity,
                'drink': History.objects.get(date=days[4], user_id=request.user).drink,
                'drink_quantity': History.objects.get(date=days[4], user_id=request.user).drink_quantity
            }
        }

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

        return JsonResponse({
            'data': data,
            'menu': menu_data
        })

    @staticmethod
    def _get_dates_in_week(date_of):
        dt = datetime.strptime(date_of, '%Y-%m-%d').date()
        start_of_week = dt - timedelta(days=dt.weekday())
        end_of_week = start_of_week + timedelta(days=4)

        dates_in_week = []
        current_date = start_of_week

        while current_date <= end_of_week:
            dates_in_week.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)

        return dates_in_week
