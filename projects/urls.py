from django.conf.urls import url, include
from django.contrib import admin

from . import views

app_name = "projects"
urlpatterns = [
    url(r'^$', views.project_list, name="project_list"),
    url(r'^(?P<project>[a-zA-Z0-9_.-]+)/(?P<rev>[a-zA-Z0-9_./-]+)$', views.project_detail, name="project_detail"),
    url(r'^(?P<project>[a-zA-Z0-9_.-]+)/(?P<rev>[a-zA-Z0-9_./-]+):inventories', include("inventories.urls")),
    url(r'^(?P<project>[a-zA-Z0-9_.-]+)/(?P<rev>[a-zA-Z0-9_./-]+):playbooks', include("playbooks.urls")),
    url(r'^(?P<project>[a-zA-Z0-9_.-]+)/(?P<rev>[a-zA-Z0-9_./-]+):tasks', include("tasks.urls")),
    
]
