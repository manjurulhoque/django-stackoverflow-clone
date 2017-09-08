from django.conf.urls import url
from .views import (
    index, ask_question, question_detail,
    category_list, category, answer_update,
    answer_delete, upvote, downvote)

urlpatterns = [
    url(r'^$', index, name='question_list'),
    url(r'^ask/$', ask_question, name='question_ask'),
    url(r'^upvote/$', upvote, name='upvote'),
    url(r'^downvote/$', downvote, name='downvote'),
    url(r'^(?P<slug>[\w-]+)/$', question_detail, name='question_detail'),
    url(r'^(?P<slug>[\w-]+)/answer/(?P<pk>\d+)/edit/$', answer_update, name='answer_update'),
    url(r'^(?P<slug>[\w-]+)/answer/(?P<pk>\d+)/delete/$', answer_delete, name='answer_delete'),
    url(r'^categories/$', category_list, name='category_list'),
    url(r'^categories/(?P<slug>[\w-]+)/$', category, name='category'),
]
