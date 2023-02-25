from rest_framework import serializers
from FilesApp.models import File

class FileSerializer(serializers.ModelSerializer):
    """
    A class to serialize file and file details to upload file.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = File
        fields = ['file_name', 'file', 'owner']
