import requests
from django.shortcuts import redirect
from django.core.files.base import ContentFile

from social.pipeline.partial import partial


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    # If there's already a user instance with an email
    if user and user.email:
        return

    # If email not in user details
    if not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            # Email not present
            # Manually ask user
            return redirect('require_email')


def save_user_photo(backend, user, response, *args, **kwargs):
    """Save Profile Picture from social accounts.
    """
    params = None

    if backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        params={'type': 'large'}
    elif backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal','')
    elif backend.name == 'google-oauth2':
        url = response['image'].get('url')
        params = {'sz': 300}
        # ext = url.split('.')[-1]
    else:
        return

    print('%'*80, url)

    try:
        response = requests.request('GET', url, params=params)
        response.raise_for_status()
    except requests.HTTPError:
        pass
    else:
        filename = '{}_social.jpg'.format(user.username)
        user.photo.save(filename, ContentFile(response.content))
        user.save()
        print('%'*100)
