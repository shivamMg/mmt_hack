import json

from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

from .models import Room
from .views import get_profile_base36

group_name = lambda label: 'profile-chat-' + label


@channel_session
@channel_session_user_from_http
def ws_connect(message):
    try:
        # `label` is base36 profile id
        prefix, _, label, _ = message['path'].strip('/').split('/')

        profile = get_profile_base36(label)

        if prefix != 'chat':
            print('Invalid WS Path (prefix not chat): %s', message['path'])
            return
        room = Room.objects.get(profile=profile)
    except ValueError:
        print('Invalid WS Path (ValueError): %s', message['path'])
        return
    except Room.DoesNotExist:
        print('WS room does not exist. Profile:', label)
        return

    print('chat connect room=%s client=%s:%s', room, message['client'][0],
          message['client'][1])

    Group(
        group_name(label),
        channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['room'] = label


@channel_session
@channel_session_user
def ws_receive(message):
    try:
        label = message.channel_session['room']
        profile = get_profile_base36(label)
        room = Room.objects.get(profile=profile)
    except KeyError:
        print('No room in channel_session')
        return
    except Room.DoesNotExist:
        print('Recieved message. But room does not exist. Profile:', label)
        return

    try:
        data = json.loads(message['text'])
    except ValueError:
        print("WS message isn't json text. Text:", message['text'])
        return

    # Data must contain message
    if set(data.keys()) != set(('message', )):
        print("WS message in unexpected format. Data:", data)
        return

    if data:
        # print('chat message room=%s message=%s', room, data['message'])
        m = room.messages.create(user=message.user, message=data['message'])

        Group(group_name(label),
              channel_layer=message.channel_layer).send(
                  {'text': json.dumps(m.as_dict())})


@channel_session
@channel_session_user
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        Group(
            group_name(label),
            channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass
