from django.shortcuts import render

from lighthouse.utils import *

from .tasks import *

# Create your views here.

def task_list(request, project, rev):
    tags, branches = get_revision(project)
    playbooks = get_playbooks(project, rev)
    inventories = get_inventories(project, rev)

    add.delay(4,4)

    return render(request, "tasks/task_list.html", {
        "project": project,
        "rev": rev,

        })

def task_detail(request, project, rev):
    pass
