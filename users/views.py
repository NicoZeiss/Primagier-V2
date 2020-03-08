from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from imagier.models import Item
from .forms import LoginForm


def user_login(request):
    """This view display login page"""
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))

                else:
                    return render(request, 'imagier/login.html', {
                        'form': form,
                        'error_message': 'Identifiant ou mot de passe incorrect'
                    })

        else:
            form = LoginForm()

        return render(request, 'imagier/login.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('index'))

def user_logout(request):
    if request.user.is_authenticated:
        temp_img = request.user.item.all()
        request.user.item.clear()
        logout(request)
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))

def save_imagier(request):
    if request.user.is_authenticated:
        pass
    else:
        return HttpResponseRedirect(reverse('index'))