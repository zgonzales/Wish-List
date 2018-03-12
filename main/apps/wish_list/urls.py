from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.success),
    url(r'^logout$', views.logout),
    url(r'^wish_items/new$', views.add),
    url(r'^wish_item/add$', views.create),
    url(r'^wish_item/item/(?P<item_id>\d+)$', views.item_info),
    url(r'^wish_item/add/(?P<item_id>\d+)$', views.join),
    url(r'^wish_item/remove/(?P<item_id>\d+)$', views.remove),
    url(r'^wish_item/delete/(?P<item_id>\d+)$', views.delete)
]