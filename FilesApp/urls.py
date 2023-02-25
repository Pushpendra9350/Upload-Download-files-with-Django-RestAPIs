from django.urls import path
from FilesApp import views

# All url patterns for FilesApp App
urlpatterns = [
    path('upload/', views.FileUploadAPI.as_view(), name="FileUpload"),
    path('list/', views.ListAllFileAPI.as_view(), name="FileList"),
    path('<int:pk>/download/', views.FileDownloadAPI.as_view(), name="FileDownload"),
]