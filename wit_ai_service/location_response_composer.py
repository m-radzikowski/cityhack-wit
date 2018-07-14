from utils.validation import Validator


class LocationResponseComposer:

    __location_response_logic_list = None
    __location_fields = ['suggested', 'confidence', 'value', 'type']

    def __init__(self, location_response_logic_list):
        if type(location_response_logic_list) is list:
            for single_logic in location_response_logic_list:
                if type(single_logic) is dict and Validator.check_if_all_keys_in(
                        single_logic, 'context', 'action'):
                    self.__location_response_logic_list = location_response_logic_list

    def check_for_locations_confidance(self, locations):
        if all (Validator.check_if_all_keys_in(location, *self.__location_fields) for location in locations):
            best_predicted = max(locations, key=lambda l: l['confidence'])
            return best_predicted
        return None


