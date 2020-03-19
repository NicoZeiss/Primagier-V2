"""Here are all the view councerning users app"""


from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from imagier.models import Favourites
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
                return render(request, 'imagier/login.html', {
                    'form': form,
                    'error_message': 'Identifiant ou mot de passe incorrect'
                })
        else:
            form = LoginForm()
        return render(request, 'imagier/login.html', {'form': form})
    return HttpResponseRedirect(reverse('index'))

def user_logout(request):
    """Log the user out"""
    if  request.user.is_authenticated:
        request.user.item.clear()
        logout(request)
        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('index'))

@login_required
def save_imagier(request):
    """Save the temp imagier as favourite"""
    if request.method == 'POST':
        form = SaveImagierForm(request.POST)
        if form.is_valid():
            imagier_title = form.cleaned_data['imagier_title']
            items = request.user.item.all().order_by('imagier_item_user.id')
            if items:
                fav_imagier = Favourites(name=imagier_title, user_id=request.user.id)
                fav_imagier.save()
                for item in items:
                    fav_imagier.item.add(item)
                request.user.item.clear()
                return HttpResponseRedirect('{}?favourite_id={}'.format(
                    reverse('users:details'),
                    fav_imagier.id))
            return HttpResponseRedirect(reverse('index'))
    else:
        form = SaveImagierForm()

    return render(request, 'imagier/save_imagier.html', {'form': form})

@login_required
def favourites(request):
    """Access to favourites template"""
    fav_filter = Favourites.objects.filter(user_id=request.user.id).order_by('name')
    fav_list = []
    for item in fav_filter:
        fav_list.append(item)
    context = {
        'favourites': fav_list,
    }
    return render(request, 'imagier/favourites.html', context)

@login_required
def details(request):
    """Display items councerning chosen favourite imagier"""
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
    """Delete an imagier from favourites"""
    fav_id = request.GET.get('favourite')
    favourite = Favourites.objects.get(id=fav_id)
    favourite.delete()

    return HttpResponseRedirect(reverse('users:favourites'))

def create_account(request):
    """Display template and form to create new account"""
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
    return HttpResponseRedirect(reverse('index'))
