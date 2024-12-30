from flask import jsonify


RESPONSE_SUCCESS = 0
RESPONSE_FAILURE = -1

class ResponseModel:

    def __init__(self, message, data): 
        self.code = 0
        self.message = message
        self.data = data

    def success_json(self):
        return jsonify({ "code": RESPONSE_SUCCESS, "message": self.message, "data": self.data })
    
    def failure_json(self):
        return jsonify({ "code": RESPONSE_FAILURE, "message": self.message, "data": self.data })


