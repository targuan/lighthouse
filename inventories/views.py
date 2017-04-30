from django.shortcuts import render
from django.http import Http404, HttpResponseBadRequest

from lighthouse.utils import *

# Create your views here.

def generic_view(request, project, rev, inventory, template=None, group=None, host=None):
    if template is None:
        template = request.resolver_match.view_name.split(':')[-1]
    groups, hosts = get_inventory(project, rev, inventory)

    if group != None and group not in groups:
        raise Http404("Group not found")
    elif group != None:
        group = groups[groups.index(group)]
    if host != None and host not in hosts:
        raise Http404("Host not found")
    elif host != None:
        host = hosts[hosts.index(host)]

    tags, branches = get_revision(project)

    return render(request, "inventories/{0}.html".format(template), {
        "project": project,
        "rev": rev,
        "inventory": inventory,
        "group": group,
        "host": host,
        "groups": groups,
        "hosts": hosts,
        "tags": tags,
        "branches": branches
        })

def inventory_list(request, project, rev):
    try:
        inventories = get_inventories(project, rev)
    except:
        raise Http404()

    tags, branches = get_revision(project)

    return render(request, "inventories/inventory_list.html", {
        "project": project,
        "rev": rev,
        "inventories": inventories,
        "tags": tags,
        "branches": branches})
