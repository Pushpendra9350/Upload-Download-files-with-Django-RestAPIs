from django.contrib.auth.models import User
from django.db import models

class File(models.Model):
    """
    Model class named a File to save files
    Fields description
    1. file_name: Store custom name of the file
    2. file: Actual file
    3. owner: Owner of the file(File uploaded by which user)
    4. is_downloaded: To make sure a user can download file only once after a new request
    5. uploaded_at: At what time this object updated
    """
    file_name = models.CharField(max_length=200, blank=False, default="", unique=True)
    file = models.FileField(upload_to='media/', blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_downloaded = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        # Will show first name as an object string
        return self.file_name

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "File"

