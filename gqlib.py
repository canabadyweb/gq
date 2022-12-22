import os
import json
import configparser

user_config_dir = os.path.expanduser("~") + "/.config/gq"
user_config_file = user_config_dir + "/gq.ini"
config = configparser.ConfigParser()


def add_section_if_not_exists(config, section_name):
    if not config.has_section(section_name):
        config.add_section(section_name)


def create_or_update_profile(user, profile, credentials):

    if credentials:
        credentials = os.path.expanduser(credentials)

        if os.path.exists(credentials):
            with open(credentials) as client_config:
                client_config_dict = json.loads(client_config.read())
                # print(client_config_dict)

                if not os.path.isfile(user_config_file):
                    os.makedirs(user_config_dir, exist_ok=True)

                installed_config = client_config_dict['installed']

                # Read config file prior to update
                config.read(user_config_file)

                add_section_if_not_exists(config, profile)
                config.set(profile, 'client_id', installed_config['client_id'])
                config.set(profile, 'client_secret',
                           installed_config['client_secret'])
                config.set(profile, 'auth_uri', installed_config['auth_uri'])
                config.set(profile, 'token_uri', installed_config['token_uri'])
                config.set(profile, 'scopes', 'https://mail.google.com/')

                # write configuration to gq.ini
                with open(user_config_file, 'w') as config_file:
                    config.write(config_file)

        else:
            print(f"Error: {credentials} doesn't exists.")


def auth(user, profile='default'):
    credentials = None

    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    import traceback

    try:
        config.read(user_config_file)

        client_id = config.get(profile, 'client_id')
        client_secret = config.get(profile, 'client_secret')
        auth_uri = config.get(profile, 'auth_uri')
        token_uri = config.get(profile, 'token_uri')
        scopes = config.get(profile, 'scopes')

        scopes_list = []
        if ',' in scopes:
            scopes_list = scopes.split(',')
        else:
            scopes_list.append(scopes)

        if config.has_section(user):
            token = config.get(user, 'token')
            refresh_token = config.get(user, 'refresh_token')
            expiry = config.get(user, 'expiry')
        else:
            (token, refresh_token, expiry) = (None, None, None)

        credentials = Credentials(
            token=token,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret,
            expiry=expiry,
        )

        if credentials and credentials.expiry and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                    client_config={
                        "installed": {
                            "client_id": client_id,
                            "client_secret": client_secret,
                            "redirect_uris": ["http://localhost",
                                              "urn:ietf:wg:oauth:2.0:oob"],
                            "auth_uri": auth_uri,
                            "token_uri": token_uri,
                        }
                    },
                    scopes=scopes_list)
            credentials = flow.run_local_server(port=0)

        add_section_if_not_exists(config, user)
        config.set(user, 'token', credentials.token)
        config.set(user, 'refresh_token', credentials.refresh_token)
        config.set(user, 'expiry', str(credentials.expiry))

        # save to a file
        with open(user_config_file, 'w') as configfile:
            config.write(configfile)

        return build('gmail', 'v1', credentials=credentials)

    except Exception as e:
        print(e)
        traceback.print_exc()
