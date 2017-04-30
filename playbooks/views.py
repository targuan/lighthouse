from django.shortcuts import render

from lighthouse.utils import *

def playbook_list(request, project, rev):
    playbooks = get_playbooks(project, rev)
    tags, branches = get_revision(project)

    return render(request, "playbooks/playbook_list.html",{
        "project": project,
        "rev": rev,
        "playbooks": playbooks,
        "tags": tags,
        "branches": branches,
    })

def playbook_detail(request, project, rev, playbook):
    playbook_content = get_playbook(project, rev, playbook)
    tags, branches = get_revision(project)

    return render(request, "playbooks/playbook_detail.html",{
        "project": project,
        "rev": rev,
        "playbook": playbook,
        "playbook_content": playbook_content,
        "tags": tags,
        "branches": branches,
        })
