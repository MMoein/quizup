from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^add/question/$', 'quiz.views.add_question', name='add_question'),
                       url(r'^add/category/$', 'quiz.views.add_category', name='add_category'),
                       url(r'^search/$', 'quiz.views.search', name='search'),
                       url(r'^challenge/(?P<quiz_id>[0-9]+)', 'quiz.views.challenge', name='challenge'),
                       url(r'^result/(?P<quiz_id>[0-9]+)', 'quiz.views.result', name='result'),
                       url(r'^(?P<quiz_id>[0-9]+)/stats', 'quiz.views.stats', name='stats'),
                       url(r'^(?P<quiz_id>[0-9]+)/select', 'quiz.views.select', name='select'),
                       url(r'^make-quiz/$', 'quiz.views.make_quiz', name='make_quiz'),
                       url(r'^scoreboard/$', 'quiz.views.scoreboard', name='scoreboard'),
                       url(r'^online-challenge/$', 'quiz.views.online_challenge', name='online_challenge'),
                       url(r'challenge-search', 'quiz.views.challenge_search', name='challenge_search'),
                       )
