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


def get_messages(service, query):
    """
       Code based on main.py from:
       https://github.com/ghaksf39/gmail-imap-login/blob/main/main.py
    """
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(
                                        userId='me', q=query,
                                        pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages


def retrieve_messages(service, messages, mark):
    """
       Code based on gmail_read.py from:
       https://github.com/abhishekchhibber/Gmail-Api-through-Python/
    """
    import base64
    from bs4 import BeautifulSoup
    import dateutil.parser as parser

    user_id = 'me'
    messages_list = []

    for message in messages:
        temp_dict = {}
        m_id = message['id']  # get id of individual message

        # fetch the message using API
        message = service.users().messages().get(userId=user_id,
                                                 id=m_id).execute()
        payld = message['payload']  # get payload of the message
        headr = payld['headers']  # get header of the payload

        for one in headr:  # getting the Subject
            if one['name'] == 'Subject':
                msg_subject = one['value']
                temp_dict['Subject'] = msg_subject
            else:
                pass

        for two in headr:  # getting the date
            if two['name'] == 'Date':
                msg_date = two['value']
                date_parse = (parser.parse(msg_date))
                m_date = (date_parse.date())
                temp_dict['Date'] = str(m_date)
            else:
                pass

        for three in headr:  # getting the Sender
            if three['name'] == 'From':
                msg_from = three['value']
                temp_dict['Sender'] = msg_from
            else:
                pass

        temp_dict['Snippet'] = message['snippet']  # fetching message snippet

        try:

            # Fetching message body
            message_parts = payld['parts']  # fetching the message parts
            part_one = message_parts[0]  # fetching first element of the part
            part_body = part_one['body']  # fetching body of the message
            part_data = part_body['data']  # fetching data from the body

            # decoding from Base64 to UTF-8
            clean_one = part_data.replace("-", "+")

            # decoding from Base64 to UTF-8
            clean_one = clean_one.replace("_", "/")

            # decoding from Base64 to UTF-8
            clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))
            soup = BeautifulSoup(clean_two, "lxml")
            message_body = soup.body()
            # message_body is a readible form of message body
            # depending on the end user's requirements,
            # it can be further cleaned
            # using regex, beautiful soup, or any other method
            temp_dict['Message_body'] = str(message_body)

        except Exception:
            pass

        # print(temp_dict)

        # This will create a dictonary item in the final list
        messages_list.append(temp_dict)

        if mark:
            # This will mark the messagea as read

            to_remove = {'removeLabelIds': ['UNREAD']}
            service.users().messages().modify(userId=user_id,
                                              id=m_id,
                                              body=to_remove).execute()

    return(messages_list)


def get_output_filename(user, query, format):
    # Replace special chars in query string with '_'
    import re
    query = re.sub(r'[^a-zA-Z0-9_\-]', '_', query)

    # Get current timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    filename = '_'.join([user, query, timestamp])
    filename = filename.replace(' ', '_')

    return '.'.join([filename, format])


def export_messages(user, query, messages_list, format, output):
    if output == 'auto':
        output = get_output_filename(user, query, format)

    if format in ['csv', 'json']:

        if format == 'json':
            with open(output, "w") as jsonfile:
                json.dump(messages_list, jsonfile, indent=6)
                print(f"Messages exported to '{output}'")

        if format == 'csv':
            with open(output, 'w', encoding='utf-8',
                      newline='\n') as csvfile:
                import csv
                fieldnames = ['Sender', 'Subject',
                              'Date', 'Snippet', 'Message_body']
                writer = csv.DictWriter(csvfile,
                                        fieldnames=fieldnames, delimiter=',')
                writer.writeheader()
                for val in messages_list:
                    writer.writerow(val)

                print(f"Messages exported to '{output}'")
    else:
        print(f"Error: Unsupported output file format: '{format}'")
