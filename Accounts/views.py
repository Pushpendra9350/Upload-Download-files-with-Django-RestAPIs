from rest_framework.views import APIView
from rest_framework import status
from Accounts.serializers import UserRegisterationSerializer
from Accounts.utils_token import get_tokens_for_user
from Accounts import serializers
from rest_framework.response import Response 
from Accounts import renderers
from django.contrib.auth import authenticate
import sys

class RegisterUserAPI(APIView):
    """
    A Class which inherits APIView class to act like an API view. And used to Register a new user.
    Have function implementation called post(), get().
    """

    # If we got error then it will render that error accordingly
    renderer_classes = [renderers.UserRenderer]

    def post(self, request, format = None):
        """
        This will handle all "POST" requests coming on this APIView
        """
        try:
            serializer = serializers.UserRegisterationSerializer(data = request.data)

            # If serialized data is valid then it will enter in this block
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()

                # Will return tokens
                token = get_tokens_for_user(user)
                return Response({"Message":"Congratulations! User created successfully", "tokens" : token}, status = status.HTTP_201_CREATED)
            return Response({"Message":serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error: " +str(e)+ " at line no. " + str(exc_tb.tb_lineno))
            return Response({"Message":"Sorry! We are facing some internal issues try agter sometime."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format = None):
        """
        This will handle all "GET" requests coming on this APIView
        """
        return Response({"Message":"Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)


class UserLoginAPI(APIView):
    """
    A Class which inherits APIView class to act like an API view. And used to Login an existing user.
    Have function implementation called post(), get().
    """

    # If we got error then it will render that error accordingly
    renderer_classes = [renderers.UserRenderer]

    def post(self, request, format = None):
        """
        This will handle all "POST" requests coming on this APIView
        """
        try:
            serializer = serializers.UserLoginSerializer(data = request.data)

            # If serialized data is valid then it will enter in this block
            if serializer.is_valid():
                username = serializer.data.get("username")
                password = serializer.data.get("password")

                # Here it will authenticate username and password
                user = authenticate(username = username, password = password)
                if user is not None:

                    # Will return tokens
                    token = get_tokens_for_user(user)
                    return Response({"Message": "LoggedIn Successfully", "tokens" : token}, status=status.HTTP_200_OK)
                else:
                    return Response({"Message": "Invalid Credentials"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"Message": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error: " +str(e)+ " at line no. " + str(exc_tb.tb_lineno))
            return Response({"Message":"Sorry! We are facing some internal issues try agter sometime."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format = None):
        """
        This will handle all "GET" requests coming on this APIView
        """
        return Response({"Message":"Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
