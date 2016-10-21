from django.shortcuts import render

from profiles.forms import SearchForm


def homepage(request):
    search_form = SearchForm()

    return render(request, 'homepage.html', {'search_form': search_form})
