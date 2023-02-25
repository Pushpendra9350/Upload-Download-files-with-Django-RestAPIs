from django.utils.encoding import smart_str
from django.http import HttpResponse

def download_file(file):
    """
    A function which help us download the file and return donwloadable content
    """
    file_content = file.file.read()
    response = HttpResponse(file_content, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{smart_str(file.file.name)}"'
    return response