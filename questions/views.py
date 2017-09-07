from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from questions.forms import QuestionForm
from .models import Category, Question


# Create your views here.


def index(request):
    questions = Question.objects.all()

    query = request.GET.get("q")
    if query:
        questions = questions.filter(
            Q(qus__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    paginator = Paginator(questions, 4)
    page = request.GET.get("page")
    try:
        query_list = paginator.page(page)
    except PageNotAnInteger:
        query_list = paginator.page(1)
    except EmptyPage:
        query_list = paginator.page(paginator.num_pages)

    context = {"query_list": query_list}
    return render(request, "questions/index.html", context)


def ask_question(request):
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        question = form.save(commit=False)
        question.user = request.user
        question.save()
        # messages.success(request, 'Question was Posted.')
        # return redirect(question.get_absolute_url())
        return redirect("/")
    context = {"form": form,
               "title": "Ask Question"
               }
    return render(request, "questions/ask.html", context)
