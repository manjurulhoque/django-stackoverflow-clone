from django.conf.urls import url
from .views import (index, ask_question)

urlpatterns = [
    url(r'^$', index, name='question_list'),
    url(r'^ask/$', ask_question, name='question_ask'),
]
