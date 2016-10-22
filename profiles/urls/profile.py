from django.conf.urls import url

from ..views import view, chat

urlpatterns = [
    url(r'^$', view, name='view'),
    url(r'^chat/$', chat, name='chat'),
]
