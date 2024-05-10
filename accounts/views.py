from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CustomUserCreationForm, CustomUserChangeForm  #, ContactFormm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.


class SignupView(UserPassesTestMixin, View):
    def get(self, request):
        if request.method == "GET":
            form = CustomUserCreationForm()
            for f in form:
                if f.label == "Password":
                    f.label = "китептин суротору"
        return render(request, 'registration/signup.html', {'forms': CustomUserCreationForm()})

    def post(self, request):
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            form.save()
            messages.success(request, 'Your account is successfully created.')
            return redirect('users:login')
        else:
            messages.info(request, "Document deleted.")
        return render(request, 'registration/signup.html', {'forms': form})

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return False
        return True


class Login(View):
    def get(self, request):
        login_form = AuthenticationForm(data=request.POST)

        return render(request, 'registration/login.html', {'forms': login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            return redirect('okuu:list_test')
        else:
            return render(request, 'registration/login.html', {'form': login_form})


@login_required
def profile(request, username):
    user = CustomUser.objects.get(username=username)
    is_owner = False

    if user == request.user:
        is_owner = True

    print(is_owner)
    return render(request, 'registration/profile.html', {"user": user})


def logout_user(request):
    logout(request)
    return render(request, 'home.html', )


# return redirect('signup')


class ProfailView(LoginRequiredMixin, View):
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        #return render(request, 'registration/profile.html',{'customuser': user})
        return render(request, 'registration/my_profile.html', {'customuser': user})


class UpdateProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = CustomUserChangeForm(instance=request.user)
        return render(request, 'registration/edit_profile.html', {'form': form})

    def post(self, request):
        form = CustomUserChangeForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account is successfully updated.')
            return redirect('users:profile', request.user)
        return render(request, 'registration/signup.html', {'form': form})
