from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from imagier.models import Item, Favourites
from .forms import LoginForm, SaveImagierForm, CreateAccountForm


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

@login_required
def user_logout(request):
    temp_img = request.user.item.all()
    request.user.item.clear()
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def save_imagier(request):
    if request.method == 'POST':
        form = SaveImagierForm(request.POST)
        if form.is_valid():
            imagier_title = form.cleaned_data['imagier_title']
            items = request.user.item.all()
            if items:
                fav_imagier = Favourites(name=imagier_title, user_id=request.user.id)
                fav_imagier.save()
                for item in items:
                    fav_imagier.item.add(item)
                request.user.item.clear()

            return HttpResponseRedirect('{}?favourite_id={}'.format(reverse('users:details'), fav_imagier.id))
    else:
        form = SaveImagierForm()

    return render(request, 'imagier/save_imagier.html', {'form': form})

@login_required
def favourites(request):
    fav_list = Favourites.objects.filter(user_id=request.user.id).order_by('name')
    favourites = []
    for item in fav_list:
        favourites.append(item)
    context = {
        'favourites': favourites,
    }
    return render(request, 'imagier/favourites.html', context)

@login_required
def details(request):
    favourite_id = request.GET.get('favourite_id')
    favourite = Favourites.objects.get(id=favourite_id)
    items = favourite.item.all()
    context = {
        'items': items,
        'favourite': favourite,
    }
    return render(request, 'imagier/details.html', context)

@login_required
def del_favourite(request):
    fav_id = request.GET.get('favourite')
    favourite = Favourites.objects.get(id=fav_id)
    favourite.delete()

    return HttpResponseRedirect(reverse('users:favourites'))

def create_account(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateAccountForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = User.objects.create_user(username, email, password)
                user.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            form = CreateAccountForm()
        return render(request, 'imagier/create_account.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('index'))