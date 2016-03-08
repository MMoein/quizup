from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^signup/$', 'Authentication.views.signup', name='signup'),
    # url(r'^login/$', 'Authentication.views.login', name='login'),
)
