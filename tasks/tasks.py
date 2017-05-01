from __future__ import absolute_import, unicode_literals
from celery import shared_task

from .models import *

@shared_task(bind=True)
def run_playbook(self, project, rev, hexsha, playbook, inventory, variables, user, password):
    task = Task.objects.get(pk=self.request.id)
    task.result = "result"
    return ""
