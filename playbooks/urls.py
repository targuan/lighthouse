from django.conf.urls import url, include
from django.contrib import admin

from . import views

app_name = "playbooks"
urlpatterns = [
    url(r'^$', views.playbook_list, name="playbook_list"),
    url(r'^/(?P<playbook>[a-zA-Z0-9_.-]+)$', views.playbook_detail, name="playbook_detail"),
]
