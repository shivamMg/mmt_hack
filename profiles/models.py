from django.db import models
from django.utils.http import int_to_base36

from users.models import User
from countries.models import Country


class Profile(models.Model):
    """Journey Profile
    """
    src_country = models.ForeignKey(Country, related_name='src_country')
    dest_country = models.ForeignKey(Country, related_name='dest_country')
    range_start = models.DateField()
    range_end = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        base36_id = int_to_base36(self.id)
        return '/journeys/p/{}'.format(base36_id)

    def __str__(self):
        return 'profile_{}'.format(self.id)
