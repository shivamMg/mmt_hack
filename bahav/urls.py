"""bahav URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from users import views as user_views

urlpatterns = [
    # Homepage
    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='homepage'),

    # User Auth
    url(
        r'^login/$',
        auth_views.login,
        name='login',
        kwargs={'template_name': 'users/login.html'},
    ),
    url(
        r'^logout/$',
        auth_views.logout,
        name='logout',
        kwargs={'next_page': '/'},
    ),
    url(
        r'^signup/$',
        user_views.signup,
        name='signup',
    ),
    url(r'^account/$', user_views.account_info, name='account'),
]
