import os
import click
import json
import traceback
import configparser
import gqlib

user_config_dir = os.path.expanduser("~") + "/.config/gq"
user_config = user_config_dir + "/gq.ini"
config = configparser.ConfigParser()


@click.command()
@click.option("-c", "--credentials",
                    help="Enter 'credentials.json' location")
@click.option("-p", "--profile",
              default='default',
              help="Profile for client config (Default: default)")
def menu(credentials, profile):

    try:
        if credentials:
            credentials = os.path.expanduser(credentials)

            if os.path.exists(credentials):
                with open(credentials) as client_config:
                    client_config_dict = json.loads(client_config.read())
                    # print(client_config_dict)

                    if not os.path.isfile(user_config):
                        os.makedirs(user_config_dir, exist_ok=True)

                    installed_config = client_config_dict['installed']

                    gqlib.add_section_if_not_exists(config, profile)
                    config.set(profile, 'client_id',
                               installed_config['client_id'])
                    config.set(profile, 'client_secret',
                               installed_config['client_secret'])
                    config.set(profile, 'token_uri',
                               installed_config['token_uri'])
                    config.set(profile, 'scope',
                               'https://mail.google.com/')

                    # write configuration to gq.ini
                    with open(user_config, 'w') as config_file:
                        config.write(config_file)

            else:
                print(f"Error: {credentials} doesn't exists.")

    except Exception as e:
        print(e)
        traceback.print_exc()


def main():
    menu()
    # Just to get prompt back in line
    print()


if __name__ == '__main__':
    main()
