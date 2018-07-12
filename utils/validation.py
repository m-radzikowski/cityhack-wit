class Validator:

    @staticmethod
    def validate_request(req_message):
        if all (k in req_message.keys() for k in ('id', 'message')):
            if type(req_message['id']) is str and type(req_message['message']) is str:
                if len(req_message['id']) > 0 and len(req_message['message']) > 0:
                    return True
            return False
