# import the User object
import re
import os
import requests

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import authentication
from rest_framework import exceptions

from radio_users.models import Profile


class GoogleOauthBackend(authentication.BaseAuthentication):
    """
    Uses a Google Oauth2 token passed in the request header.
    Retreives or creates a user object, based on their email domain
    """
    def authenticate(self, request):
        # Retrieve the access token from the request header
        access_token = request.META.get('HTTP_X_GOOGLE_AUTH_TOKEN')
        if access_token:
            print access_token
            # Validated the token and pull down the user details
            params = {'alt': 'json', 'access_token': access_token}
            r = requests.get(
                'https://www.googleapis.com/oauth2/v1/userinfo',
                params=params
            )
            person = r.json()

            # Ensure a valid json object is returned
            if person.get('error') or person['verified_email'] is False:
                print person.get('error')
                raise exceptions.AuthenticationFailed(
                    person['error']['message']
                )

            # Retrieve the whitelisted domains set in the .env file
            domains = os.environ.get('GOOGLE_WHITE_LISTED_DOMAINS', '')
            white_listed_domains = re.findall('([a-z\.]+)', domains)

            # Ensure the users domain exists within the whilelist
            if person['hd'] not in white_listed_domains:
                print 'Invalid domain' + person['hd']
                raise exceptions.AuthenticationFailed('Invalid domain')

            password = make_password(person['id'])
            try:
                user = User.objects.get(email=person['email'])
            except:
                print 'user not found'
                try:
                    user = User.objects.create(
                        username=person['name'],
                        password=password,
                        first_name=person['given_name'],
                        last_name=person['family_name'],
                        email=person['email']
                    )
                    Profile.objects.create(
                        user=user,
                        avatar=person['picture']
                    )
                except:
                    print 'User could not be created'
                    raise exceptions.AuthenticationFailed(
                        'User could not be created'
                    )

            return (user, None)
        print 'no access_token provided'
        return None
