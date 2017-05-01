import os
import re
from git import *
from git.util import join_path
from git.repo.base import is_git_dir

from inventories.models import *

from django.conf import settings

def _get_repo(project):
    try:
        return Repo(os.path.join(settings.PROJECTS_PATH, project))
    except:
        raise Exception("Project not found")

def _get_tree(project, rev):
    repo = _get_repo(project)
    try:
        return repo.tree(rev)
    except:
        raise Exception("Revision {0} not found".format(rev))

def resolve_rev(project, rev):
    repo = _get_repo(project)
    try:
        return repo.commit(rev).hexsha
    except:
        raise Exception("Revision {0} not found".format(rev))

def get_projects():
    projects = [p for p in os.listdir(settings.PROJECTS_PATH)
                    if is_git_dir(os.path.join(settings.PROJECTS_PATH,p))
                    or is_git_dir(os.path.join(settings.PROJECTS_PATH,p,'.git'))]
    return projects

def get_inventories(project, rev):
    tree = _get_tree(project, rev)

    inventories = []
    try:
        inventories_tree = tree["inventories"]
        for tree in inventories_tree.trees:
            if join_path(tree.path, "hosts") in tree:
                inventories.append(tree.name)
    except:
        pass

    return inventories

def parse_inventory(content):
    group_re = re.compile('^\[([^\]:]+)\]$')

    groups = []
    group = Group('all')
    groups.append(group)

    hosts = []
    host = ''
    for line in content.replace('\r','\n').split('\n'):
        line = line.strip()
        if not line:
            continue
        m = group_re.match(line)
        if m:
            group = Group(m.group(1))
            if group not in groups:
                groups.append(group)
        else:
            host = Host(line.split()[0])
            try:
                i = hosts.index(host)
                host=hosts[i]
            except:
                hosts.append(host)

            groups[0].add_host(host)
            group.add_host(host)
    group = Group('ungrouped')
    groups.append(group)
    for host in groups[0].hosts:
        if len(host.groups) == 1:
            host.add_group(group)
    return groups, hosts

def get_inventory(project, rev, inventory):
    tree = _get_tree(project, rev)

    try:
        inventory_tree = tree["inventories"][inventory]
    except:
        raise Exception("Inventory {0} not found".format(inventory))

    if "inventories/{0}/{1}".format(inventory, "hosts") not in inventory_tree:
        raise Exception("hosts file not found in ".format(inventory))

    host_file = inventory_tree['hosts']
    hosts_content = host_file.data_stream.read().decode('utf-8')

    groups, hosts = parse_inventory(hosts_content)

    group_vars = []
    if "inventories/{0}/group_vars".format(inventory) in inventory_tree:
        group_vars_tree = inventory_tree["group_vars"]
        for group in groups:
            for ext in ["",".yml",".yaml"]:
                if "inventories/{0}/group_vars/{1}{2}".format(inventory, group.name,ext) in group_vars_tree:
                   group.variables = group_vars_tree[group.name + ext].data_stream.read().decode('utf-8')
                   break

    if "inventories/{0}/host_vars".format(inventory) in inventory_tree:
        host_vars_tree = inventory_tree['host_vars']
        for host in hosts:
            for ext in ["",".yml",".yaml"]:
                if "inventories/{0}/host_vars/{1}{2}".format(inventory, host.name, ext) in host_vars_tree:
                    host.variables = host_vars_tree[host.name + ext].data_stream.read().decode('utf-8')
                    break

    return groups, hosts

def get_revision(project):
    repo = _get_repo(project)

    tags = map(lambda x:x.name, repo.tags)
    branches = map(lambda x:x.name, repo.branches)

    return tags, branches

def get_playbooks(project, rev):
    tree = _get_tree(project, rev)

    playbooks = []
    try:
        playbooks_tree = tree["playbooks"]
        for blob in playbooks_tree.blobs:
            playbooks.append(blob.name)
    except:
        pass

    return playbooks

def get_playbook(project, rev, playbook):
    tree = _get_tree(project, rev)
    try:
        playbooks_blob = tree["playbooks/{0}".format(playbook)]
    except:
        raise Exception("Playbook {0} not found".format(playbook))

    return playbooks_blob.data_stream.read().decode('utf-8')


