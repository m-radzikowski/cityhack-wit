from wit import Wit
from utils.validation import Validator 



class WitService:
    
    @staticmethod
    def compose_response(message_from_wit, msg_id):
        if 'entities' in message_from_wit.keys() and 'sentiment' in message_from_wit['entities'].keys():
            for sugestion in message_from_wit['entities']['sentiment']:
                if all (k in sugestion.keys() for k in ('confidence','value')):
                    return {
                        'confidence': sugestion['confidence'],
                        'value': sugestion['value'].upper(),
                        'id': msg_id
                        }
        return None
    
    def __init__(self, access_token):
        self.__client = Wit(access_token)

    def write_to(self, message_to):
        if Validator.validate_request(message_to):
            msg_text = message_to['message']
            msg_text_length = len(msg_text)
            print(f' ## MESSAGE: {msg_text}')
            if msg_text_length in range(0, 250):
                wit_response = self.__client.message(msg_text)
                return WitService.compose_response(wit_response, message_to['id'])
        return None
 
