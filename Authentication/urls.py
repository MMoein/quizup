from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^signup/$', 'Authentication.views.signup', name='signup'),
    url(r'^verify/(?P<token>.*)/$', 'Authentication.views.verify', name='verify'),
    url(r'^login/$', 'Authentication.views.login', name='login'),
)
