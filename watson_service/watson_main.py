from wit_ai_service.wit_ai_main import MainWitService
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException
from utils.validation import Validator



class WatsonService:
    
    __content_type = 'application/json'

    @staticmethod
    def compose_response(msg, msg_id):
        if 'document_tone' in msg.keys() and 'tones' in msg['document_tone'].keys():
            tones = msg['document_tone']['tones']
            if type(tones) is list and len(tones) > 0:
                return {
                    'tones': tones
                }
        return None

    def __init__(self, version, api_key):
        self.__watson_service = ToneAnalyzerV3(version=version, iam_api_key=api_key)
    
    def write_to(self, message_to):
        if Validator.validate_request(message_to):
            msg_text = message_to['message']
            tone = self.__watson_service({'text': msg_text}, self.__content_type)
        return None
 
