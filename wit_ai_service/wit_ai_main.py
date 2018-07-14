from wit import Wit
from wit_ai_service.location_response_composer import LocationResponseComposer
from utils.validation import Validator


class WitService(LocationResponseComposer):
    
    @staticmethod
    def compose_response(message_from_wit, msg_id):
        if 'entities' in message_from_wit.keys():
                if'sentiment' in message_from_wit['entities'].keys():
                    for sugestion in message_from_wit['entities']['sentiment']:
                        if all (k in sugestion.keys() for k in ('confidence','value')):
                            return {
                            'confidence': sugestion['confidence'],
                            'value': sugestion['value'].upper(),
                            'id': msg_id
                            }
        return None
    
    def __init__(self, access_token, location_response_logic_list):
        super().__init__(location_response_logic_list)
        self.__client = Wit(access_token)


    def write_to(self, message):
        msg_text = message['message']
        msg_text_length = len(msg_text)
        print(' ## MESSAGE: {}'.format(msg_text))
        if msg_text_length in range(0, 250):
            wit_response = self.__client.message(msg_text)
            print(' ## WIT RESPONDED: ')
            print(wit_response)
            return WitService.compose_response(wit_response, message['id'])
        return None

    def talk_to(self, message):
        msg_text = message['message']
        msg_text_length = len(msg_text)
        print(' ## MESSAGE: {}'.format(msg_text))
        if msg_text_length in range(0, 250):
            wit_response = self.__client.message(msg_text)
            print(wit_response)
            if 'entities' in wit_response.keys():
                return self.__create_response_to_msg(wit_response['entities'])
        return None

    def __create_response_to_msg(self, wit_response):
        if Validator.check_if_any_keys_in(wit_response, 'location'):
            return self.check_for_locations_confidance(wit_response['location'])
        return None



