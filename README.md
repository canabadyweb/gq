# gq 

> Gmail Query CLI

## Install

#### Clone the repository
```sh
$ git clone https://github.com/canabadyweb/gq
```

#### Move into the gq folder
```sh
$ cd gq
```

#### Create Python Virtual Environment
```sh
$ python3 -m venv .
```

#### Start the virtual environment by “sourcing” the activate script.
```sh
$ source ./bin/activate
```
or
```sh
$ . ./bin/activate
```

#### (First time only) Install requirements inside the virtual environment:
```sh
$ pip install -r requirements.txt
```

#### Run the application
```sh
$ python3 gq.py --help
````

It will output the usage options for ```gq.py```
```
Usage: gq.py [OPTIONS]

Options:
  -c, --credentials TEXT  Enter 'credentials.json' location
  -p, --profile TEXT      Profile for client config (Default: default)
  -u, --user TEXT         Label for Gmail username
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

#### Prior to querying Gmail, we have to load ```credentails.json``` using -c option. 
(Need only for first time or if we want to change the credentials)
See: 
[How to get Google Client ID and Client Secret?](https://www.balbooa.com/gridbox-documentation/how-to-get-google-client-id-and-client-secret) for more information on how to create and download credentials.json.

```sh
$ python3 gq.py -c credentails.json
```
> Note: JSON file name can be any name but the content should have the same structure as that of from Google.


#### Add a gmail account to gq
```sh
$ python3 gq.py -u <ACCOUNT_NAME>
```
> Note: <ACCOUNT_NAME> is label for the account to be authorized

This will ask you to do authorization with a Google account.

After successful authorization, the output will show the number of unread messages in that Gmail account
```
Query ('is:unread') matches 0 message(s)
```


#### To find number of mails from google to <ACCOUNT_NAME>
```sh
$ python3 gq.py -u <ACCOUNT_NAME> -q 'from: google'
```

Query accepts [Search operators you can use with Gmail](https://support.google.com/mail/answer/7190?hl=en)


#### To retrieve the queried messages
```sh
$ python3 gq.py -u <ACCOUNT_NAME> -q <Any_Search_Query> -r
```
This will output the messages in the console. To export them to a file, we need to used -e option


#### To mark the queried messages as READ
```sh
$ python3 gq.py -u <ACCOUNT_NAME> -q <Any_Search_Query> -r -m
```

> Note: For mark messages as READ to work, we need to give gmail modify  permission in oAuth consent screen in developer console.


#### To export the retrieved message
```sh
$ python3 gq.py -u <ACCOUNT_NAME> -q <Any_Search_Query> -r -e
```

This will export the messages to ACCOUNT_NAME_QUERY-STRING_DATE-STAMP.csv file in the current directory. To save it to other location, we need to pass -o option
```sh
$ python3 gq.py -u <ACCOUNT_NAME> -q <Any_Search_Query> -r -e -o '/tmp/my_mail_messsages.csv'
```


#### To export the retrieved message in JSON format
```sh
$ python3 gq.py -u <ACCOUNT_NAME> -q <Any_Search_Query> -r -e -f json
```
> Note: Only CSV (default) and JSON format is supported.


#### To use multiple credentials.json, we can use -p (profile) option
```sh
$ python3 gq.py -c credentails.json -p <PROFILE_NAME>
```

To use profile other then default, we need to pass it while we do user auth process with google account
```sh
$ python3 gq.py -p <PROFILE_NAME> -u <ACCOUNT_NAME>
```
