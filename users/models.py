from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from countries.models import Country


class UserManager(BaseUserManager):
    def create_user(self, username, email, country="1", password=None):
        if not username:
            raise ValueError('User must have a username')
        if not email:
            raise ValueError('User must have an email')
        if not country:
            raise ValueError('User must have a country')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.country = Country.objects.get(pk=country)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, country, password):
        user = self.create_user(username=username,
                                email=email,
                                country=country,
                                password=password)
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.SlugField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=15, blank=True)
    middle_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=15, blank=True)

    country = models.ForeignKey(Country)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_absolute_url(self):
        return '/account/'

    def get_full_name(self):
        return '{} {} {}'.format(self.first_name, self.middle_name,
                                 self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        """User belongs to staff if he is an admin or superuser"""
        return self.is_admin or self.is_superuser
