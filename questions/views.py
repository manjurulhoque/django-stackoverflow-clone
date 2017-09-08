from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from questions.forms import QuestionForm, AnswerForm
from .models import Category, Question, Answer, Vote


# Create your views here.


def index(request):
    questions = Question.objects.all()

    query = request.GET.get("q")
    if query:
        questions = questions.filter(
            Q(questions__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    paginator = Paginator(questions, 2)
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


def question_detail(request, slug=None):
    global user_authenticated
    global this_user
    this_user = False
    question = get_object_or_404(Question, slug=slug)
    vote_count = Vote.objects.filter(question_id=question.id).count()
    print(vote_count)
    answers_list = Answer.objects.filter(question=question)
    if request.user.is_anonymous:
        user_authenticated = False
    else:
        user_authenticated = True
    context = {"question": question,
               "answers_list": answers_list,
               "user_authenticated": user_authenticated,
               "vote_count": vote_count,
               "this_user": this_user
               }
    if request.user.is_authenticated:
        form = AnswerForm(request.POST or None)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            # messages.success(request, 'Answer was Posted.')
            form = AnswerForm()
            v = Vote.objects.filter(user_id=request.user.id)
            if v:
                user_authenticated = True
                this_user = True
            else:
                user_authenticated = False
                this_user = False
        context = {"question": question,
                   "form": form,
                   "answers_list": answers_list,
                   "user_authenticated": user_authenticated,
                   "vote_count": vote_count,
                   "this_user": this_user
                   }
    return render(request, "questions/question_detail.html", context)


def category_list(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "questions/category_list.html", context)


def category(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    queryset = category.question_set.all()

    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(
            Q(qus__icontains=query)
        ).distinct()

    paginator = Paginator(queryset, 12)
    page = request.GET.get("page")
    try:
        query_list = paginator.page(page)
    except PageNotAnInteger:
        query_list = paginator.page(1)
    except EmptyPage:
        query_list = paginator.page(paginator.num_pages)

    context = {"query_list": query_list,
               "category": category
               }
    return render(request, "questions/category.html", context)


@login_required()
def answer_update(request, slug=None, pk=None):
    question = get_object_or_404(Question, slug=slug)
    instance = get_object_or_404(Answer, pk=pk)
    if instance.user != request.user:
        raise Http404
    else:
        form = AnswerForm(request.POST or None, instance=instance)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            # messages.success(request, 'Answer was Updated.')
            return redirect(question.get_absolute_url())
        context = {"form": form,
                   "title": "Update Answer"
                   }
    return render(request, "questions/answer.html", context)


@login_required()
def answer_delete(request, slug=None, pk=None):
    question = get_object_or_404(Question, slug=slug)
    answer = get_object_or_404(Answer, pk=pk)
    if not request.user.is_authenticated:
        raise Http404
    else:
        if answer.user != request.user:
            raise Http404
        else:
            answer.delete()
            # messages.error(request, 'Answer was Deleted.')
            return redirect(question.get_absolute_url())


@login_required()
@csrf_exempt
def upvote(request):
    print(request.POST['value'])
    return JsonResponse({'status': 'ok'})


@login_required()
def downvote(request):
    pass