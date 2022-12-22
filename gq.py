import os
import click
import json
import traceback
import configparser

user_config_dir = os.path.expanduser("~") + "/.config/gq"
user_config = user_config_dir + "/gq.ini"
config = configparser.ConfigParser()


def add_section_if_not_exists(config, section_name):
    if not config.has_section(section_name):
        config.add_section(section_name)


@click.command()
@click.option("-c", "--credentials",
                    help="Enter 'credentials.json' location")
def menu(credentials):

    try:
        if credentials:
            credentials = os.path.expanduser(credentials)

            if os.path.exists(credentials):
                with open(credentials) as client_config:
                    client_config_dict = json.loads(client_config.read())
                    print(client_config_dict)

                    if not os.path.isfile(user_config):
                        os.makedirs(user_config_dir, exist_ok=True)

                    installed_config = client_config_dict['installed']

                    add_section_if_not_exists(config, 'gq')
                    config.set('gq', 'client_id',
                               installed_config['client_id'])
                    config.set('gq', 'client_secret',
                               installed_config['client_secret'])
                    config.set('gq', 'token_uri',
                               installed_config['token_uri'])
                    config.set('gq', 'scope',
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
