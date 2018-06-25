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
        print(' ## Configuration has been set.')
    else:
        raise Exception(' ## Configuration is not set or unaccesable, check you config.json file.')

def set_dependencies():
    global configuration
    global wit_service
    if 'wit_ai' in configuration.keys() and 'access_token' in configuration['wit_ai'].keys():
        access_token = configuration['wit_ai']['access_token']
        wit_service = MainWitService(access_token)

def get_wit_response(message_to_wit):
    resp = wit_service.write_to(message_to_wit)
    suggested = []
    print(resp)
    if 'entities' in resp.keys() and 'reference' in resp['entities'].keys():
        for sugestion in resp['entities']['reference']:
            if all (k in sugestion.keys() for k in ('confidence','value')):
                suggested.append({'confidance': sugestion['confidence'], 'value': sugestion['value']})
    return suggested

@app.route('/')
def main():
    return 'Hello from Wit Api, your endpoint for sending messages to validate is http://api_ip_address/message'



class MessageHandler(Resource):
    def post(self):
        wit_message = request.get_json(force=True)
        print(wit_message)
        wit_resonses = get_wit_response('Tak jeszcze kosciol mi tu postawcie!')
        if wit_resonses is not None:
            return 200, json.dumps(wit_resonses)
        else:
            abort(404, message="Data sent {} are in wrong format.".format(wit_message))


api.add_resource(MessageHandler, '/message')


if __name__ == '__main__':
    read_configuation()
    set_dependencies()
    app.run(debug=True, host='0.0.0.0')
