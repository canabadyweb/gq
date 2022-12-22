import os
import click
import json
import traceback


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
