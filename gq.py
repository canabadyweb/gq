import click
import traceback
import gqlib


@click.command()
@click.option("-c", "--credentials",
                    help="Enter 'credentials.json' location")
@click.option("-p", "--profile",
              default='default',
              help="Profile for client config (Default: default)")
@click.option("-u", "--user",
              default=None,
              help="Gmail username")
def menu(user, profile, credentials):

    try:
        if credentials:
            gqlib.create_or_update_profile(user, profile, credentials)

        if user:
            gqlib.auth(user, profile)

    except Exception as e:
        print(e)
        traceback.print_exc()


def main():
    menu()
    # Just to get prompt back in line
    print()


if __name__ == '__main__':
    main()
