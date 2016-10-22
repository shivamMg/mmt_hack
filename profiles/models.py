from django.db import models
from django.utils import timezone
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
        return '/j/{}'.format(base36_id)

    def __str__(self):
        return 'profile_{}'.format(self.id)


class Room(models.Model):
    """Chat Room
    """
    profile = models.OneToOneField(Profile)
    members = models.ManyToManyField(User)

    def __str__(self):
        return 'Room for: ' + str(self.profile)


class Message(models.Model):
    """Chat Message
    """
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    room = models.ForeignKey(Room, related_name='messages')
    user = models.ForeignKey(User)

    def __str__(self):
        return self.id

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'user': self.user.email,
                'message': self.message,
                'timestamp': self.formatted_timestamp}
