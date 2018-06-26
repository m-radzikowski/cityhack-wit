from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import json
from wit_ai_service.wit_ai_main import MainWitService

app = Flask(__name__)
api = Api(app)
configuration = None
wit_service = None

def read_configuation():
    global configuration
    configuration = json.loads(open('config.json', 'r').read())
    if configuration is not None:
        print(' ## Configuration has been read.')
    else:
        raise Exception(' ## Configuration is not set or unaccesable, check you config.json file.')

def set_dependencies():
    global configuration
    global wit_service
    if 'wit_ai' in configuration.keys() and 'access_token' in configuration['wit_ai'].keys():
        access_token = configuration['wit_ai']['access_token']
        wit_service = MainWitService(access_token)
        print(' ## Connected to wit.ai')
    else:
        raise Exception(' ## Configuretion file has wrong format or structure. Should be json file.')

@app.route('/')
def main():
    return 'Hello from Wit Api, your endpoint for sending messages to validate is http://api_ip_address/message. JSON format is: {"id": string, "message": string}'



class MessageHandler(Resource):
    global wit_service
    def post(self):
        client_ip_address = request.remote_addr
        req = request.get_json(force=True)
        print('************************* NEW REQUEST *************************')
        print(f' ## Requst form ip address: {client_ip_address}')
        wit_resonse = wit_service.write_to(req)
        confidence, value = wit_resonse['confidence'], wit_resonse['value']
        print(f' ## RESPONSE: confidane : {confidence}, value: {value}')
        return wit_resonse


api.add_resource(MessageHandler, '/message')


if __name__ == '__main__':
    read_configuation()
    set_dependencies()
    app.run(debug=True, host='0.0.0.0')
