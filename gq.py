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
              help="Label for Gmail username")
@click.option("-q", "--query",
              default="is:unread",
              help="""Gmail search query
              More info: https://support.google.com/mail/answer/7190?hl=en""")
@click.option("-r", "--retrieve",
              is_flag=True,
              help="Retrieve message that matches the query")
@click.option("-m", "--mark",
              is_flag=True,
              help="Mark messages as READ that matches the query")
@click.option("-e", "--export",
              is_flag=True,
              help="Export retrieved messages")
@click.option("-f", "--format",
              default='csv',
              help="Output file format. Possible values are [csv, json]")
@click.option("-o", "--output",
              default='auto',
              help="Output filename to export retrieved messages")
def menu(user, profile, credentials, query, retrieve,
         mark, export, format, output):

    try:
        if credentials:
            gqlib.create_or_update_profile(user, profile, credentials)

        if user:
            if format not in ['csv', 'json']:
                print(f"Error: Unsupported output file format: '{format}'")
            else:
                service = gqlib.auth(user, profile)
                messages = gqlib.get_messages(service, query)

                num_messages = len(messages)

                print(f"Query ('{query}') matches {num_messages} message(s)")

                if retrieve:
                    print(f"Retrieving {num_messages} messages...")

                    messages_list = gqlib.retrieve_messages(service,
                                                            messages, mark)

                    if export:
                        gqlib.export_messages(user, query,
                                              messages_list, format, output)
                    else:
                        print(messages_list)

    except Exception as e:
        print(e)
        traceback.print_exc()


def main():
    menu()
    # Just to get prompt back in line
    print()


if __name__ == '__main__':
    main()
