# gq 

> Gmail Query CLI

## Install

#### Clone the repository
```
$ git clone https://github.com/canabadyweb/gq
```

#### Move into the gq folder
```s
$ cd gq
```

#### Create Python Virtual Environment
```
$ python3 -m venv .
```

#### Start the virtual environment by “sourcing” the activate script.
```
$ source ./bin/activate
```
or
```
$ . ./bin/activate
```

#### (First time only) Install requirements inside the virtual environment:
```
$ pip install -r requirements.txt
```

#### Run the application
```
$ python3 gq.py --help
````

It will output the usage options for ```gq.py```
```
Usage: gq.py [OPTIONS]

Options:
  -c, --credentials TEXT  Enter 'credentials.json' location
  -p, --profile TEXT      Profile for client config (Default: default)
  -u, --user TEXT         Gmail username
  -q, --query TEXT        Gmail search query More info:
                          https://support.google.com/mail/answer/7190?hl=en
  -r, --retrieve          Retrieve message that matches the query
  -m, --mark              Mark messages as READ that matches the query
  -e, --export            Export retrieved messages
  -f, --format TEXT       Output file format. Possible values are [csv, json]
  -o, --output TEXT       Output filename to export retrieved messages
  --help                  Show this message and exit.
```

## Usage

#### Prior to querying Gmail, we have load ```credentails.json``` using -c option. 
(Need only for first time or if we want to change the credentials)
See: 
[How to get Google Client ID and Client Secret?](https://www.balbooa.com/gridbox-documentation/how-to-get-google-client-id-and-client-secret)

for more information to create and download credentials.json.
```
$ python3 gq.py -c credentails.json
```
> Note: JSON file name can have any title, not need to be only as `credentials.json`

#### Add a gmail account to gq
```
$ python3 gq.py -u <ACCOUNT_NAME>
```
> Note: <ACCOUNT_NAME> is label for the account to be authorized

This will ask you to do authorization with a Google account.

After successful authorization, the output will show the number of unread messages in that Gmail account
```
Query ('is:unread') matches 0 message(s)
```

#### To find number of mails from google to <ACCOUNT_NAME>
```
$ python3 gq.py -u <ACCOUNT_NAME> -q 'from: google'
```

Query accepts [Search operators you can use with Gmail](https://support.google.com/mail/answer/7190?hl=en)


#### To retrieve the queried messages
```
$ python3 gq.py -u <ACCOUNT_NAME> -q <Any_Search_Query> -r
```
This will output the messages in the console. To export them to a file, we need to used -e option


#### To mark the queried messages as READ
```
$ python3 gq.py -u <ACCOUNT_NAME> -q <Any_Search_Query> -r -m
```

> Note: For mark messages as READ to work, we need to give gmail modify  permission in oAuth consent screen in developer console.


#### To export the retrieved message
```
$ python3 gq.py -u <ACCOUNT_NAME> -q <Any_Search_Query> -r -e
```

This will export the messages to ACCOUNT_NAME_QUERY-STRING_DATE-STAMP.csv file in the current directory. To save it to other location, we need to pass -o option
```
$ python3 gq.py -u <ACCOUNT_NAME> -q <Any_Search_Query> -r -e -o '/tmp/my_mail_messsages.csv'
```

#### To export the retrieved message in JSON format
```
$ python3 gq.py -u <ACCOUNT_NAME> -q <Any_Search_Query> -r -e -f json
```
> Note: Only CSV (default) and JSON format is supported.


#### To use multiple credentials.json, we can use -p (profile) option
```
$ python3 gq.py -c credentails.json -p profile1
```

To use for profile other then default, we need to pass it while we do user auth process with google account
```
$ python3 gq.py -p profile1 -u <ACCOUNT_NAME>
```
