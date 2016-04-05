from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^add/question/$', 'quiz.views.add_question', name='add_question'),
                       url(r'^add/category/$', 'quiz.views.add_category', name='add_category'),
                       url(r'^search/$', 'quiz.views.search', name='search'),
                       )
