from wit import Wit
import re

class MainWitService:
    def __init__(self, access_token):
        self.__client = Wit(access_token)

    def write_to(self, message_to):
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
        if self.__validate_request(message_to):
            filtered_message = emoji_pattern.sub(r'', message_to['message'])
            print(f' ## MESSAGE NOT FILTRED {message_to}')
            print(f' ## MESSAGE FILTRED: {filtered_message}')
            if len(filtered_message) > 0 and len(filtered_message) < 250:
                wit_response = self.__client.message(filtered_message)
                print(f' ## RESPONSE: {wit_response}')
                return self.__validate_wit_response(wit_response, message_to['id'])
        return {
            'confidence': 0.0,
            'value': 'NOT_FOUND',
            'id': message_to['id']
            }

    def __validate_wit_response(self, message_from_wit, msg_id):
        if 'entities' in message_from_wit.keys() and 'sentiment' in message_from_wit['entities'].keys():
            for sugestion in message_from_wit['entities']['sentiment']:
                if all (k in sugestion.keys() for k in ('confidence','value')):
                    return {
                        'confidence': sugestion['confidence'],
                        'value': sugestion['value'].upper(),
                        'id': msg_id
                        }
        return {
        'confidence': 0.0,
        'value': 'NOT_FOUND',
        'id': msg_id
        }

    def __validate_request(self, req_message):
        if all (k in req_message.keys() for k in ('id', 'message')):
            if type(req_message['id']) is str and type(req_message['message']) is str:
                if len(req_message['id']) > 0 and len(req_message['message']) > 0:
                    return True
        return False
