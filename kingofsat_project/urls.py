
from django.conf.urls import url, include

from views import scaner, post_kingofsat, channel_post, channel_list, list, filterview, simple_list, dataTabs

urlpatterns = [

    url(r'^$', post_kingofsat, name="index"),
    url(r'^kingofsat$', scaner, name="kingofsat"),
    url(r'^kingofsat$', channel_list, name="kingofsat"),
    url(r'^post/channel/$', channel_post, name="post_channel"),
    url(r'^list/$', list, name="list"),
    url(r'^filter/$', filterview, name="filter"),
    url(r'^djangotabs/$', simple_list, name="djangotabs"),
    url(r'^datatable/$', dataTabs, name="datatable"),
]

