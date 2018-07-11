from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import json
import sys
from wit_ai_service.wit_ai_main import MainWitService
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException

app = Flask(__name__)
api = Api(app)
configuration = None
wit_service = None
watson = None

def read_configuation():
    global configuration
    configuration = json.loads(open('config.json', 'r').read())
    if configuration is not None:
        print(' ## Configuration has been read.')
    else:
        raise Exception(' ## Configuration is not set or unaccesable, check you config.json file.')

def set_witai_dependencies():
    global configuration
    global wit_service
    if 'wit_ai' in configuration.keys() and 'access_token' in configuration['wit_ai'].keys():
        access_token = configuration['wit_ai']['access_token']
        wit_service = MainWitService(access_token)
        print(' ## Connected to wit.ai')
    else:
        raise Exception(' ## Configuretion file has wrong format or structure. Should be json file.')

def set_watson_dependencies():
    # TODO set in separate class like wit_service with validation
    global configuration
    global watson_service
    if 'watson' in configuration.keys() and all (k in configuration['watson'].keys() for k in ('version', 'iam_api_key')):
        version = configuration['watson']['version']
        api_key = configuration['watson']['iam_api_key']
        watson_service = ToneAnalyzerV3(version=version, iam_api_key=api_key)

@app.route('/')
def main():
    return 'Hello from Sentiment Recogintion API, your endpoint for sending messages for validation is http://api_ip_address/message. JSON format is: {"id": string, "message": string}'



class MessageHandler(Resource):
    global wit_service
    def post(self):
        client_ip_address = request.remote_addr
        req = request.get_json(force=True)
        print('************************* NEW REQUEST *************************')
        print(f' ## Requst from ip address: {client_ip_address}')
        if wit_service is not None:
            wit_resonse = wit_service.write_to(req)
            confidence, value = wit_resonse['confidence'], wit_resonse['value']
            print(f' ## RESPONSE: confidane : {confidence}, value: {value}')
            return wit_resonse, 200
        elif watson_service is not None:
            try:
                message = req['message']
                content_type = 'application/json'
                tone = watson_service.tone({'text': message}, content_type)
                # TODO: handle tone and return proper format
                return {'confidance': '_', 'value': '_'}, 200
            except WatsonApiException as ex:
                print(f'Method failed with status code {str(ex.code)}: {ex.message}')
        return 'Internal api server issue', 500


api.add_resource(MessageHandler, '/message')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        read_configuation()
        if sys.argv[1] == 'witai':    
            set_witai_dependencies()
            app.run(debug=True, host='0.0.0.0')
        elif sys.argv[1] == 'watson':
            pass
        else:
            print('Wrong NPL api name.')
    else:
        print('NPL api name hasn\'t been provided, "witai" or "watson" are avaliable options.')

