from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm

from .forms import UserCreationForm, UserChangeForm


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('login'))

    return render(request, 'users/signup.html', {'form': form})


@login_required
def account_info(request):
    if request.method == 'GET':
        form = UserChangeForm(
            instance=request.user,
            initial={'country': request.user.country.code}
        )
    elif request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    return render(request, 'users/account.html', {'form': form})

def require_email(request):
    try:
        backend = request.session['partial_pipeline']['backend']
    except KeyError:
        return HttpResponseNotFound()

    form = AuthenticationForm()
    return render(request, 'users/login.html', {
        'form': form,
        'backend': backend,
        'require_email': True,
    })
