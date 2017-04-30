from django.conf.urls import url, include
from django.contrib import admin

from . import views

app_name = "tasks"
urlpatterns = [
    url(r'^$', views.task_list, name="list"),
    url(r'^/(?P<task>[a-zA-Z0-9_.-]+)$', views.task_detail, name="detail"),
]
