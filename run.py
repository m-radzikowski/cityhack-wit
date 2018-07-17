from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import json
import sys
from watson_service.watson_main import WatsonService
from wit_ai_service.wit_ai_main import WitService
from utils.validation import Validator
from utils.logger import Logger


app = Flask(__name__)
api = Api(app)
configuration = None
location_response_logic_list = None
wit_service = None
watson_service = None


def read_configuation():
    global configuration
    global location_response_logic_list
    try:
        configuration = json.loads(open('config.json', 'r').read())
    except:
        Exception('config file does not exists.')
    try:
        location_response_logic_list = json.loads(open('bot_logic/location_logic.json', 'r').read())
    except:
        Exception('bot location logic file does not exists.')
    if configuration is not None:
        print(' ## Configuration has been read.')
    else:
        raise Exception(' ## Configuration is not set or unaccesable, check you config.json file.')

def set_witai_dependencies():
    global configuration
    global location_response_logic_list
    global wit_service
    if 'wit_ai' in configuration.keys() and 'access_token' in configuration['wit_ai'].keys():
        access_token = configuration['wit_ai']['access_token']
        wit_service = WitService(access_token, location_response_logic_list)
        print(' ## Connected to wit.ai')
    else:
        raise Exception(' ## Configuretion file has wrong format or structure. Should be json file.')

def set_watson_dependencies():
    global configuration
    global watson_service
    if 'watson' in configuration.keys() and all (k in configuration['watson'].keys() for k in ('version', 'username', 'password', 'url')):
        version = configuration['watson']['version']
        username = configuration['watson']['username']
        password = configuration['watson']['password']
        url = configuration['watson']['url']
        watson_service = WatsonService(version, username, password, url)

@app.route('/')
def main():
    return '''
        Hello from Sentiment Recogintion API,
        your endpoint for sending messages for validation
        is http://api_ip_address/message. JSON format is: {"id": string, "message": string}
        '''


class SentimentHandler(Resource):
    global wit_service
    def post(self):
        # TODO: start session for each client
        client_ip_address = request.remote_addr
        req = request.get_json(force=True)
        Logger.client_ip(client_ip_address)
        if wit_service and Validator.validate_request(req) is not None:
            wit_response = wit_service.write_to(req)
            if wit_response is not None:
                return wit_response, 200
            return {
                'confidence': 0.0,
                'value': 'NOT_FOUND',
                'id': req['id']
                } 
        elif watson_service is not None:
            watson_response = watson_service.write_to(req)
            print(watson_response)
            if watson_response is not None:
                return watson_response, 200
            return 'Response not found', 404
        return 'Internal api server issue', 500



class ConversationHandler(Resource):
    global wit_service
    def post(self):
        # TODO: start session for conversation
        client_ip_address = request.remote_addr
        req = request.get_json(force=True)
        Logger.client_ip(client_ip_address)
        if wit_service is not None and Validator.validate_request(req):
            wit_response = wit_service.talk_to(req)
            if wit_response is not None:
                return wit_response, 200
            return wit_response
        elif watson_service is not None and Validator.validate_request(req):
            # watson_response = watson_service.talk_to(req)
            pass
            return {'id': req['id'], 'message': 'not implemented at this point'}
        return 'Internal api server issue', 500



api.add_resource(SentimentHandler, '/sentiment')
api.add_resource(ConversationHandler, '/conversation')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        read_configuation()
        if sys.argv[1] == 'witai':    
            set_witai_dependencies()
        elif sys.argv[1] == 'watson':
            set_watson_dependencies()
        else:
            print('Wrong NPL api name.')
        app.run(debug=True, host='0.0.0.0')
    else:
        print('NPL api name hasn\'t been provided, "witai" or "watson" are avaliable options.')
    
