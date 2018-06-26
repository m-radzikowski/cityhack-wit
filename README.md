# Main information:

This API is written in Python3.6

# Clone from git

Write in terminal: ```$git clone https://github.com/m-radzikowski/cityhack-wit.git```

# Installation & run server

Use Python3.6 or greater

Write in terminal: ```$python3.6 -m venv venv/```

Open virtual environment writing in terminal: ```$source venv/bin/activate```

Install dependencies writing in terminal: ```$pip install -r requirements.txt```

Write in terminal ```$python server.py```

# Endpoints

## Posting messages and sentiment validation:

Send POST request to http://server_ip_address:5000/messages
Request Header: Content-Type: application/json
Request Body:
```json
{
  "id": string that is identifying message,
  "message": string text to validate sentiment
}
```
