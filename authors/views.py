from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

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

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(
        request,
        'authors/pages/login.html',
        {
            'form': form,
            'form_action': reverse('authors:login_create')
        })


def login_create(request):
    # Redirecting to 404 page if there's no POST data
    if not request.POST:
        raise Http404

    # Instantiating form with POST data
    form = LoginForm(request.POST)
    # Login template URL
    login_url = reverse('authors:login_register')

    # Form is valid. Trying authenticate user
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', None),
            password=form.cleaned_data.get('password', None),
        )
        # User is authenticated. Logging in and defining sucess message
        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, 'You are logged in')
        # User is not authenticated. Defining error message
        else:
            messages.error(request, 'Invalid credentials')
    # Form is not valid. Redirecting to login page with errors
    else:
        messages.error(request, 'Invalid username or password')

    # Redirecting to login page
    return redirect(login_url)
