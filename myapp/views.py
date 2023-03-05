from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserLogin


class User:

    @staticmethod
    def home(request):

        return render(request, 'home.html')

    @staticmethod
    def log_in(request):

        if request.method == 'POST':

            form = UserLogin(request.POST)

            if form.is_valid():

                return HttpResponseRedirect('home')

            else:

                return HttpResponseRedirect('login')

        else:

            form = UserLogin()

        return  render(request, 'login.html', {'form': form})
