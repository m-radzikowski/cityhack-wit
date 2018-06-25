from flask import Flask
import json
from wit_ai_service.wit_ai_main import MainWitService

app = Flask(__name__)
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
    wit_resonses = get_wit_response('Tak jeszcze kosciol mi tu postawcie!')
    for wit_response in wit_resonses:
        value = wit_response['value']
        confidance = wit_response['confidance']
        print(f'Response value: {value}')
        print(f'Response confidance is: {confidance}')
    return 'Hello from Flask - Wit application'


if __name__ == '__main__':
    read_configuation()
    set_dependencies()
    app.run(debug=True)
