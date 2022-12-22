import os
import click
import json
import traceback
import gqlib


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

                    if not os.path.isfile(gqlib.user_config):
                        os.makedirs(gqlib.user_config_dir, exist_ok=True)

                    installed_config = client_config_dict['installed']

                    gqlib.add_section_if_not_exists(gqlib.config, profile)
                    gqlib.config.set(profile, 'client_id',
                                     installed_config['client_id'])
                    gqlib.config.set(profile, 'client_secret',
                                     installed_config['client_secret'])
                    gqlib.config.set(profile, 'token_uri',
                                     installed_config['token_uri'])
                    gqlib.config.set(profile, 'scope',
                                     'https://mail.google.com/')

                    # write configuration to gq.ini
                    with open(gqlib.user_config, 'w') as config_file:
                        gqlib.config.write(config_file)

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
