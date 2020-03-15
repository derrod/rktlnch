#!/usr/bin/env python
# coding: utf-8

import argparse
import subprocess
import json
import os
import shlex
from sys import exit as _exit

from base64 import b64decode, b64encode

from src.epic_api import EPCAPI
from src.epic_lfs import EPCLFS


def exit(code=0):
    input('Press enter to exit.')
    _exit(code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch an EGS game without EGS.')

    group = parser.add_mutually_exclusive_group()
    group.required = True
    group.add_argument('--launch', dest='app_name', action='store',
                       help='Launch game with codename APP_NAME')
    group.add_argument('--list-games', dest='list_games', action='store_true',
                       help='List installed app names and their corresponding game names.')

    parser.add_argument('--skip-version-check', dest='skip_version_check', action='store_true',
                        default=False, help='Skip version check')

    args, extra = parser.parse_known_args()

    elfs = EPCLFS()

    try:
        # read config with auth data
        print('Reading EGS config... ', end='', flush=True)
        elfs.read_config()
        remember_me_data = elfs.config.get('RememberMe', 'Data')
        re_data = json.loads(b64decode(remember_me_data))[0]
        if 'Token' not in re_data:
            raise ValueError('No login session in config')
        print('[OK]')

        # read manifests of installed games
        print('Getting installed games... ', end='', flush=True)
        elfs.read_manifests()
        print('[OK]')
    except Exception as e:
        print('[FAIL]\nReading manifests/config failed with:', repr(e))
        exit(1)

    if args.list_games:
        game_manifests = elfs.manifests.values()

        print('Installed games (game name => app name):')
        for game in sorted(game_manifests, key=lambda a: a['DisplayName'].lower()):
            print('* Game:', game['DisplayName'], '=>', game['AppName'])

        print('Use the app name with the --launch parameter')
        _exit(0)

    # check if we know the game id
    try:
        print(f'Checking manifest for "{args.app_name}" ', end='', flush=True)
        game_manifest = elfs.get_manifest(game_name=args.app_name.strip())
        print('[OK]')
    except Exception as e:
        print(f'[FAIL]\nCannot find game manifest for {args.app_name}:', repr(e))
        exit(1)

    eapi = EPCAPI()

    try:
        print('Logging into EGS... ', end='', flush=True)
        auth_data = eapi.start_session(re_data['Token'])
        print(f'[OK]\nLogged in as "{auth_data["displayName"]}"!')

        print('Saving new refresh token... ', end='', flush=True)
        # try saving the new refresh token
        re_data['Token'] = auth_data['refresh_token']
        remember_me_data = b64encode(json.dumps([re_data]).encode('utf-8')).decode('utf-8')
        elfs.config.set('RememberMe', 'Data', remember_me_data)
        elfs.save_config()
        print('[OK]')
    except Exception as e:
        print('[FAIL]\nFailed to refresh token with:', repr(e))
        exit(1)

    if not args.skip_version_check:
        print('Checking game version... ', end='', flush=True)
        try:
            versions = eapi.get_game_versions()
            installed_ver = game_manifest['AppVersionString']

            for ver in versions:
                if ver['catalogItemId'] == game_manifest['CatalogItemId']:
                    if installed_ver != ver['buildVersion']:
                        print(f'[FAIL]\nGame is outdated ({installed_ver} != {ver["buildVersion"]}), '
                              f'please launch EGS and update the game.')
                        exit(0)
            else:
                print('[OK]')

        except Exception as e:
            print('[FAIL]\nCould not get game versions:', repr(e))
            exit(1)

    try:
        print('Getting game oauth token... ', end='', flush=True)
        game_token = eapi.get_game_token()
        print('[OK]')
    except Exception as e:
        print('[FAIL]\nFailed to get game token with:', repr(e))
        exit(1)

    exe_path = os.path.join(game_manifest['InstallLocation'],
                            game_manifest['LaunchExecutable'])

    params = [exe_path,
              '-AUTH_LOGIN=unused',
              f'-AUTH_PASSWORD={game_token["code"]}',
              '-AUTH_TYPE=exchangecode',
              f'-epicapp={game_manifest["AppName"]}',
              '-epicenv=Prod',
              '-EpicPortal',
              f'-epicusername={auth_data["displayName"]}',
              f'-epicuserid={auth_data["account_id"]}',
              '-epiclocale=en']

    # add params from manifest (required for e.g. Fornite)
    if game_manifest.get('LaunchCommand', ''):
        print('Adding "LaunchCommand" from manifest...')
        params.extend(shlex.split(game_manifest['LaunchCommand']))

    # allow passing params through to the game
    if extra:
        print('Adding extra params:', ', '.join(extra))
        params.extend(extra)

    try:
        # Launching the game!
        print('Launching the game... ', end='', flush=True)
        subprocess.Popen(params, cwd=game_manifest['InstallLocation'])
        print('[OK!]')
    except Exception as e:
        print('[FAIL]\nFailed to launch game:', repr(e))
        exit(1)

    _exit(0)
