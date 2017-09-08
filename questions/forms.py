from django import forms
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question", "details", "category"]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["ans"]