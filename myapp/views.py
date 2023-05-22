from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.views.generic import CreateView, TemplateView
from django.views.generic import UpdateView
from .forms import ProfileUpdateForm, OrderForm, AddMenuForm, MainPageForm


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
    FormSet = formset_factory(OrderForm, extra=5)
    template_name = "myapp/order.html"
    success_url = reverse_lazy("order_success")

    def get(self, request, *args, **kwargs):
        current_page = request.session.get("current_page", 1)
        formset = self.FormSet(initial=[{}] * current_page)
        return render(request, self.template_name, {'formset': formset, 'current_page': current_page})

    def post(self, request, *args, **kwargs):

        formset = self.FormSet(request.POST)
        current_page = int(request.POST.get("current_page", 1))

        if formset.is_valid():

            next_page = current_page + 1

            if next_page <= 5:
                request.session["current_page"] = next_page
                return redirect("order_page")
            else:
                del request.session['current_page']
                return redirect("order_success")

        return render(request, self.template_name, {
            'formset': formset,
            'current_page': current_page
        })
