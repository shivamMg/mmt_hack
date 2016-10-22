from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import base36_to_int

from profiles.forms import SearchForm, CreationForm
from profiles.models import Profile, Room
from users.models import User


def get_profile_base36(base36_id):
    """Returns Profile using base36 profile id
    """
    int_id = base36_to_int(base36_id)
    profile = get_object_or_404(Profile, id=int_id)
    return profile


@login_required
@csrf_exempt
def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            options = dict()
            options['src_country'] = form.clean_src_country()
            options['dest_country'] = form.clean_dest_country()
            departure_date = form.cleaned_data['departure_date']

            profile_list = Profile.objects.filter(
                range_start__lt=departure_date,
                range_end__gt=departure_date,
                **options)

            return render(request, 'profiles/search.html',
                          {'profile_list': profile_list,
                           'search_form': form})
        else:
            print(form.errors)
            return render(request, 'homepage.html', {'search_form': form})
    else:
        return HttpResponseRedirect('/')


@login_required
def create(request):
    if request.method == 'GET':
        form = CreationForm()
    elif request.method == 'POST':
        form = CreationForm(request.POST)

        if form.is_valid():
            user = User.objects.get(username=request.user)
            profile = form.save(commit=False)
            profile.creator = user
            profile.save()
            return HttpResponseRedirect(profile.get_absolute_url())

    return render(request, 'profiles/create.html', {'form': form})


@login_required
def view(request, profile_id):
    profile = get_profile_base36(profile_id)

    return render(request, 'profiles/view.html', {'profile': profile})


def chat(request, profile_id):
    profile = get_profile_base36(profile_id)

    room, _ = Room.objects.get_or_create(profile=profile)
    message_list = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, 'profiles/chat_room.html',
                  {'message_list': message_list})
