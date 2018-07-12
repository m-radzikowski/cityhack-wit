# Main information:

This API is written in Python3.6

# Clone from git

Write in terminal:
```
$git clone https://github.com/m-radzikowski/cityhack-wit.git
```

# Installation & run server

Use Python3.6 or greater

Write in terminal:
```
$python3.6 -m venv venv/
```

Open virtual environment writing in terminal:
```
$source venv/bin/activate
```

Install dependencies writing in terminal:
```
$pip install -r requirements.txt
```

Write in terminal
```
$python server.py
```

# Endpoints

## Posting messages and sentiment validation:

Send POST request to:
```
http://server_ip_address:5000/message
```
Request Header:
```
Content-Type: application/json
```
Request Body:
```json
{
  "id": "string that is identifying message",
  "message": "string text to validate sentiment"
}
```

# Config:

Your '''config.json''' should look like this:

'''
{
  	"wit_ai": {
      		"access_token": "C7X6YA4UQCLI64CDCWC2VJAD4UV4B6GD"
    },
    "watson": {
            "url": "https://gateway.watsonplatform.net/tone-analyzer/api",
            "username": "1eeacd3f-bcd8-4d1d-a481-7e26fa2c2e2f",
            "password": "7xOUxb2rblIq",
			"version": "2017-09-21"
	}
}
'''

