from django.db import models
from base.models import Basemodel

class User(Basemodel):
    user_id = models.AutoField(primary_key=True)
    mail = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # You should store hashed passwords!

    def __str__(self):
        return self.username


class Filestore(Basemodel):
    file_id = models.AutoField(primary_key=True)
    file_uploaded = models.FileField(upload_to='uploads/')
    date_of_file_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File {self.file_id} uploaded on {self.date_of_file_upload}"


class ColdMail(Basemodel):
    coldmail_id = models.AutoField(primary_key=True)
    gen_response = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(Filestore, on_delete=models.CASCADE)

    def __str__(self):
        return f"ColdMail {self.coldmail_id} for User {self.user.username}"
