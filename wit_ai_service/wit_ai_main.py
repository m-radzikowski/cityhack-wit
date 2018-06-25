from wit import Wit

class MainWitService:
    def __init__(self, access_token):
        self.__client = Wit(access_token)

    def write_to(self, message_to):
        response_from_wit = self.__client.message(message_to)
        return self.__validate_wit_response(response_from_wit)

    def __validate_wit_response(self, message_to_wit):
        suggested = []
        print(message_to_wit)
        if 'entities' in message_to_wit.keys() and 'reference' in message_to_wit['entities'].keys():
            for sugestion in message_to_wit['entities']['reference']:
                if all (k in sugestion.keys() for k in ('confidence','value')):
                    suggested.append({'confidance': sugestion['confidence'], 'value': sugestion['value']})
        return suggested
