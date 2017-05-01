from django.db import models

class Task(models.Model):
    task_id = models.CharField(max_length=50, primary_key=True)
    project = models.CharField(max_length=50)
    rev = models.CharField(max_length=50)
    hexsha = models.CharField(max_length=40)
    playbook = models.CharField(max_length=50)
    inventory = models.CharField(max_length=50)
    variables = models.TextField()
    user = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    result = models.TextField()

