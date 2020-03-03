#!/usr/bin/env python
# coding: utf-8

import requests
from requests.auth import HTTPBasicAuth


class EPCAPI:
    _user_agent = 'UELauncher/10.13.1-11497744+++Portal+Release-Live Windows/10.0.18363.1.256.64bit'
    # required for the oauth request
    _user_basic = '34a02cf8f4414e29b15921876da36f9a'
    _pw_basic = 'daafbccc737745039dffe53d94fc76cf'

    _oauth_host = 'account-public-service-prod03.ol.epicgames.com'
    _launcher_host = 'launcher-public-service-prod06.ol.epicgames.com'

    def __init__(self):
        self.session = requests.session()
        self.session.headers['User-Agent'] = self._user_agent
        self._oauth_basic = HTTPBasicAuth(self._user_basic, self._pw_basic)

        self.access_token = None
        self.user = None

    def start_session(self, refresh_token):
        params = dict(grant_type='refresh_token',
                      refresh_token=refresh_token,
                      token_type='eg1')

        r = self.session.post(f'https://{self._oauth_host}/account/api/oauth/token',
                              data=params, auth=self._oauth_basic)

        r.raise_for_status()
        self.user = r.json()
        self.session.headers['Authorization'] = f'bearer {self.user["access_token"]}'
        return self.user

    def invalidate_session(self):  # unused
        r = self.session.delete(f'https://{self._oauth_host}/account/api/oauth/sessions/kill/{self.access_token}')

    def get_game_token(self):
        r = self.session.get(f'https://{self._oauth_host}/account/api/oauth/exchange')
        r.raise_for_status()
        return r.json()

    def get_game_versions(self):
        r = self.session.get(f'https://{self._launcher_host}/launcher/api/public/assets/Windows',
                             params=dict(label='Live'))
        r.raise_for_status()
        return r.json()
