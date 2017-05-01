from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from lighthouse.utils import *

from .tasks import *
from .models import *

import yaml

# Create your views here.

def task_list(request, project, rev):
    tasks = Task.objects.all()

    tags, branches = get_revision(project)
    playbooks = get_playbooks(project, rev)
    inventories = get_inventories(project, rev)

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "project": project,
        "rev": rev,
        "tags": tags,
        "branches": branches,
        "inventories": inventories,
        "playbooks": playbooks
        })

def task_detail(request, project, rev, task):
    tags, branches = get_revision(project)
    playbooks = get_playbooks(project, rev)
    inventories = get_inventories(project, rev)

    task = get_object_or_404(Task, pk = task)
    return render(request, "tasks/detail.html", {
        "task":task,
        "project": project,
        "rev": rev,
        "tags": tags,
        "branches": branches,
        "inventories": inventories,
        "playbooks": playbooks
        })


def task_create(request, project, rev):
    playbooks = get_playbooks(project, rev)
    inventories = get_inventories(project, rev)

    if request.method == 'POST':
        playbook = request.POST['playbook']
        if playbook not in playbooks:
            raise Http404("Playbook not found")
        
        inventory = request.POST['inventory']
        if inventory not in inventories:
            raise Http404("Inventory not found")
        
        variables = request.POST['variables']
        try:
            yaml.load(variables)
        except:
            raise Http404("Variables are not in yaml format")

        user = ""
        password = ""

        hexsha = resolve_rev(project, rev)
        result = run_playbook.delay(project, rev, hexsha, playbook, inventory, variables, user, password)
        task = Task(task_id=result.task_id,
                    project=project,
                    rev=rev,
                    hexsha=hexsha,
                    playbook=playbook,
                    inventory=inventory,
                    variables=variables,
                    user=user
                    )
        task.save()

        return redirect("projects:tasks:detail", project=project, rev=rev, task=result.task_id)
    
    tags, branches = get_revision(project)

    return render(request, "tasks/task_create.html", {
        "project": project,
        "rev": rev,
        "tags": tags,
        "branches": branches,
        "inventories": inventories,
        "playbooks": playbooks
        })
