from flask_restful import Resource


class DefaultResource(Resource):
    def get(self):
        return {
            "status": "success",
            "data": {
                "msg": "Successful setup test response"
            }
        }