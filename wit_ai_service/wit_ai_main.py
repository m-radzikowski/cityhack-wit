from wit import Wit

class MainWitService:
    def __init__(self, access_token):
        self.__client = Wit(access_token)

    def write_to(self, message_to):
        if self.__validate_request(message_to):
            wit_response = self.__client.message(message_to['message'])
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
                return True
        return False
