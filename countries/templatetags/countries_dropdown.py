from django_jinja import library

from countries.models import Country


@library.global_function
def list_countries():
    country_list = Country.objects.all()
    return country_list
