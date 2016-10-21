from django.conf.urls import url

from .views import search, create, view

urlpatterns = [
    url(r'^search/$', search, name='search'),
    url(r'^create/$', create, name='create'),
    url(r'^p/(?P<profile_id>[a-z0-9]+)/', view, name='view'),
]
