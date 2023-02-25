from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from FilesApp.models import File
from django.shortcuts import render
from Accounts import renderers
from django.contrib.auth import authenticate
from Accounts.serializers import UserLoginSerializer
from django.conf import settings
from FilesApp.utils import download_file
from FilesApp.serializers import FileSerializer
import sys

class FileUploadAPI(APIView):
    """
    A Class which act like an API view. And used to upload a file.
    Have function implementation called post(), get().
    """

    # If we got error then it will render that error accordingly
    renderer_classes = [renderers.UserRenderer]

    # Will Authenticate wheather user is authorized or not to upload file
    # If not authorized then it will return from here
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        """
        This will handle all "POST" requests coming on this APIView
        """
        try:
            # will check file existance otherwise return from here
            if not request.data.get('file'):
                return Response({'Message': 'Missing file data.'}, status=status.HTTP_400_BAD_REQUEST)

            file_serializer = FileSerializer(data=request.data)

            # If file serialization valid then file will be saved
            if file_serializer.is_valid():
                file_serializer.save(owner=request.user)
                return Response({'Message': 'Congratulations! File uploaded successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error: " +str(e)+ " at line no. " + str(exc_tb.tb_lineno))
            return Response({"Message":"Sorry! We are facing some internal issues try agter sometime."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format = None):
        """
        This will handle all "GET" requests coming on this APIView
        """
        return Response({"Message":"Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

class ListAllFileAPI(APIView):
    """
    A Class act like an API view. And used to list all files owned by this perticular user.
    Have function implementation called post(), get().
    """

    # If we got error then it will render that error accordingly
    renderer_classes = [renderers.UserRenderer]

    # Will Authenticate wheather user is authorized or not to upload file
    # If not authorized then it will return from here
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        This will handle all "GET" requests coming on this APIView
        In this function will fetch all files owned by user and process them and then send back to user as a result
        """
        try:
            file_list = []
            files = File.objects.filter(owner=request.user)
            if files.count() > 0:
                files.update(is_downloaded=False)
                for file in files:
                    file_dict = {}
                    file_dict["File name"] = file.file_name
                    file_dict["Download link"] = settings.HOST_URL + "file/" + str(file.pk) + "/download"
                    file_list.append(file_dict)
                return Response({'Message': 'Here is the list of all files link! Paste link in you browser to download the file.', 'files': file_list}, status=status.HTTP_200_OK)
            else:
                return Response({'Message': 'Sorry! We did not found any files owned by this user'}, status=status.HTTP_200_OK)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error: " +str(e)+ " at line no. " + str(exc_tb.tb_lineno))
            return Response({"Message":"Sorry! We are facing some internal issues try agter sometime."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, format = None):
        """
        This will handle all "POST" requests coming on this APIView
        """
        return Response({"Message":"Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)


class FileDownloadAPI(APIView):
    """
    A Class act like an API view. And used to download a file requested by the user.
    Have function implementation called post(), get().
    """
    def get(self, request, pk):
        """
        This will handle all "GET" requests coming on this APIView
        In this function we will check wheather file is downloadable or not 
        And if user authenticated then download the file.
        """
        try:
            try:
                file = File.objects.get(pk=pk)
                if file.is_downloaded == True:
                    return Response({"Message":"You have already downloaded the file! To download it again you have to raise a request again"}, status=status.HTTP_403_FORBIDDEN)
            except ObjectDoesNotExist:
                return Response({"Message":"File not found 1"}, status=status.HTTP_404_NOT_FOUND)

            # Check wheater user is authenticated or not
            if not request.user.is_authenticated:
                return render(request, "FilesApp/get_token.html", {'file_name': file.file_name, "file_id": file.pk})
            else:
                # Will return downloadable content
                response = download_file(file)
                file.is_downloaded = True
                file.save()
                return response
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error: " +str(e)+ " at line no. " + str(exc_tb.tb_lineno))
            return Response({"Message":"Sorry! We are facing some internal issues try agter sometime."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, pk):
        """
        This will handle all "POST" requests coming on this APIView
        In this function we will get username and password from the user to authenticate user to downlaod secured files.
        After authication it will automatically downlaod the file.
        """
        try:
            serializer = UserLoginSerializer(data = request.data)

            # If data is serialized and valid
            if serializer.is_valid():
                username = serializer.data.get("username")
                password = serializer.data.get("password")

                # Authenticate user with username and password
                user = authenticate(username = username, password = password)
                if user is not None:
                    try:
                        file = File.objects.get(pk=pk)
                        if file.is_downloaded == True:
                            return Response({"Message":"You have already downloaded the file! To download it again you have to raise a request again"}, status=status.HTTP_403_FORBIDDEN)
                    except ObjectDoesNotExist:
                        return Response({"Message":"File not found"}, status=status.HTTP_404_NOT_FOUND)
                    
                    # Will return downloadable content
                    response = download_file(file)
                    file.is_downloaded = True
                    file.save()
                    return response
                else:
                    return Response({"Message": "Invalid Credentials"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"Message": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error: " +str(e)+ " at line no. " + str(exc_tb.tb_lineno))
            return Response({"Message":"Sorry! We are facing some internal issues try agter sometime."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)