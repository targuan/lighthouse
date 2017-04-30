from django.conf.urls import url, include
from django.contrib import admin

from . import views

app_name = "inventories"
urlpatterns = [
    url(r'^$', views.inventory_list, name="inventory_list"),
    url(r'^/(?P<inventory>[a-zA-Z0-9_.-]+)$', views.generic_view, name="inventory_detail"),
    url(r'^/(?P<inventory>[a-zA-Z0-9_.-]+)/groups$', views.generic_view, name="group_list"),
    url(r'^/(?P<inventory>[a-zA-Z0-9_.-]+)/groups/(?P<group>[a-zA-Z0-9_.-]+)$', views.generic_view, name="group_detail"),
    url(r'^/(?P<inventory>[a-zA-Z0-9_.-]+)/hosts$', views.generic_view, name="host_list"),
    url(r'^/(?P<inventory>[a-zA-Z0-9_.-]+)/hosts/(?P<host>[a-zA-Z0-9_.-]+)$', views.generic_view, name="host_detail"),
]
