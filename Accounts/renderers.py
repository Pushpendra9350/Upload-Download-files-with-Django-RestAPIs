from rest_framework.renderers import JSONRenderer
import json

class UserRenderer(JSONRenderer):
    """
    A Class with a function called render to format our error messages to get better understanding & formating for end user.
    """
    charset = "utf-8"
    def render(self, data, accepted_media_type = True, renderer_context = None):
        response = ""

        # Will check "ErrorDetail" is in the data if yes then it has some error and then format it
        if "ErrorDetail" in str(data):
            response = json.dumps({"error": data})
        else:
            response = json.dumps(data)
        return response