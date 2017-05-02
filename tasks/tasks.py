from __future__ import absolute_import, unicode_literals
from celery import shared_task

import os

from .models import *
from git import *
from lighthouse.utils import *

import subprocess
import time
import io

@shared_task(bind=True)
def run_playbook(self, project, rev, hexsha, playbook, inventory, variables, user, password, options):
    task = Task.objects.get(pk=self.request.id)
    tmp_dir = os.path.join('/tmp', task.task_id)
    repo = get_repo(project)
    repo.clone(tmp_dir)
    g = Repo(tmp_dir).git
    g.checkout(hexsha)

    playbook_path = os.path.join(tmp_dir, 'playbooks', playbook)
    inventory_path = os.path.join(tmp_dir, 'inventories', inventory,'hosts')

    ansible = ["/opt/ansible_venv/bin/ansible-playbook",
        #"--version"]
        playbook_path,
        '-i', inventory_path,
        '-e', variables]

    if options.get('check', False):
        ansible.append('--check')

    if options.get('limit', ''):
        ansible += ['--limit', options['limit']]

    print(ansible)
        
    
    out = open(tmp_dir + '.out', 'w')
    err = open(tmp_dir + '.err', 'w')
    p = subprocess.Popen(ansible, 
        stdout=out, 
        stdin=subprocess.PIPE, 
        stderr=err,
        cwd=tmp_dir)
    ret_code = p.poll()
    while ret_code is None:
        time.sleep(0.5)
        ret_code = p.poll()
        result = open(tmp_dir + '.out').read()
        task.result = result
        task.save()
    print(task.result)
    print(ret_code)
    task.result = "result"
    return ""
