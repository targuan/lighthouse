import os

from django.shortcuts import render
from django.conf import settings
from django.http import Http404

from git.repo.base import is_git_dir
from git.util import join_path
from git import *

from lighthouse.utils import get_inventories, get_projects


# Create your views here.
def project_list(request):
    projects = get_projects()
    projects.sort()
    return render(request, 'projects/project_list.html', {'projects': projects})



def project_detail(request, project, rev):
    projects = get_projects()
    if not project in projects:
        raise Http404("Project not found")

    repo = Repo(os.path.join(settings.PROJECTS_PATH, project))
    try:
        base_tree = repo.tree(rev)
    except:
        raise Http404("Revision {0} not found".format(rev))



    inventories = get_inventories(project, rev)
    playbooks = []
    try:
        playbooks_tree = base_tree["playbooks"]

        for blob in playbooks_tree.blobs:
            playbooks.append(blob.name)
    except:
        pass

    tags = map(lambda x:x.name, repo.tags)
    branches = map(lambda x:x.name, repo.branches)
    return render(request, 'projects/project_detail.html', {'project': project, 'rev': rev, 'inventories': inventories, "playbooks": playbooks, "tags": tags, "branches": branches})


