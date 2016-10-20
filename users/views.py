from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

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
