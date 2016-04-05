from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^add_question/$', 'quiz.views.add_question', name='add_question'),
    url(r'^add_category/$', 'quiz.views.add_category', name='add_category'),
    # url(r'^verify/(?P<token>.*)/$', 'Authentication.views.verify', name='verify'),
    # url(r'^login/$', 'Authentication.views.login', name='login'),
)
