import logging
import json

class DefectDojoResponse(object):
    """
    Container for all DefectDojo API responses, even errors.

    """

    def __init__(self, message, success, logger_name, data=None, response_code=-1):
        self.message = message
        self.data = data
        self.success = success
        self.response_code = response_code
        self.logger = logging.getLogger(logger_name)

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return self.message

    def id(self):
        self.logger.debug("response_code" + str(self.response_code))
        if self.response_code == 400: #Bad Request
            raise ValueError('Object not created:' + json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': ')))
        return int(self.data["id"])

    def count(self):
        return self.data["count"]

    def data_json(self, pretty=False):
        """Returns the data as a valid JSON string."""
        if pretty:
            return json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            return json.dumps(self.data)