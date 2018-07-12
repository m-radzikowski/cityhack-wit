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

Your ```config.json``` should look like JSON below:

This is fake:
```
{
  	"wit_ai": {
      		"access_token": "CS554564FDFGERGE34534DFDFS34534"
    },
    "watson": {
            "url": "https://gateway.watsonplatform.net/tone-analyzer/api",
            "username": "123123-12fwef-2312in-1231mnkn-13132",
            "password": "123sdfs123d342fsdf43",
			"version": "2017-09-21"
	}
}
```

