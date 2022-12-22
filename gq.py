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
@click.option("-q", "--query",
              default="is:unread",
              help="""Gmail search query
              More info: https://support.google.com/mail/answer/7190?hl=en""")
@click.option("-e", "--export",
              is_flag=True,
              help="Export retrieved messages")
@click.option("-f", "--format",
              default='csv',
              help="Output file format. Possible values are [csv, json]")
@click.option("-o", "--output",
              default='auto',
              help="Output filename to export retrieved messages")
def menu(user, profile, credentials, query, export, format, output):

    try:
        if credentials:
            gqlib.create_or_update_profile(user, profile, credentials)

        if user:
            service = gqlib.auth(user, profile)
            messages = gqlib.get_messages(service, query)

            print(f"Query ('{query}') matches {len(messages)} message(s)")

            messages_list = gqlib.retrieve_messages(service, messages)
            # print("Total messaged retrieved: ", str(len(messages_list)))
            # print(messages_list)

            if export:
                gqlib.export_messages(user, query,
                                      messages_list, format, output)

    except Exception as e:
        print(e)
        traceback.print_exc()


def main():
    menu()
    # Just to get prompt back in line
    print()


if __name__ == '__main__':
    main()
