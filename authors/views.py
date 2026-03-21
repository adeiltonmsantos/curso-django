from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from recipes.models import Recipe

from .forms import LoginForm, RegisterForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request,
                  'authors/pages/register_view.html',
                  context={
                      'form': form,
                      'form_action': reverse('authors:register_create'),
                  }
                  )


def register_create(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in.')
        del (request.session['register_form_data'])
        return redirect(reverse('authors:login_register'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(
        request,
        'authors/pages/login.html',
        {
            'form': form,
            'form_action': reverse('authors:login_create'),
            'form_action_logout': reverse('authors:logout'),
        })


def login_create(request):
    # Redirecting to 404 page if there's no POST data
    if not request.POST:
        raise Http404

    # Instantiating form with POST data
    form = LoginForm(request.POST)

    # Form is valid. Trying authenticate user
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        # User is authenticated. Logging in and defining sucess message
        if authenticated_user is not None:
            messages.success(request, 'You are logged in')
            login(request, authenticated_user)
        # User is not authenticated. Defining error message
        else:
            messages.error(request, 'Invalid credentials')
            return redirect(reverse('authors:login_register'))
    # Form is not valid. Redirecting to login page with errors
    else:
        messages.error(request, 'Invalid username or password')
        return redirect(reverse('authors:login_register'))

    # Redirecting to login page
    return redirect(reverse('authors:dashboard'))


@login_required(
    login_url='authors:login',
    redirect_field_name='next'
)
def logout_view(request):
    # Checking if there's POST data. If not, redirecting to login page
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login_register'))

    # Checking if user is authenticated. if not, redirect to login page
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login_register'))

    messages.success(request, 'You are logged out.')
    logout(request)
    return redirect(reverse('authors:login_register'))


@login_required(
    login_url='authors:login',
    redirect_field_name='next'
)
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(
        request,
        'authors/pages/dashboard.html',
        context={
            'recipes': recipes,
        }
    )
