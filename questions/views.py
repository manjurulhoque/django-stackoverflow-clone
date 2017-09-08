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
    global upvote, downvote, vote_count
    same_user = False
    upvote = False
    downvote = False
    question = get_object_or_404(Question, slug=slug)
    votes = Vote.objects.filter(question_id=question.id)
    vote_count = votes.filter(Q(upvote__exact=1) | Q(downvote__exact=1)).count()
    # print(vote_count)
    answers_list = Answer.objects.filter(question=question)
    context = {"question": question,
               "answers_list": answers_list,
               "vote_count": vote_count,
               "same_user": same_user,
               "upvote": upvote,
               "downvote": downvote
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
        try:
            v = Vote.objects.get(question_id=question.id, user_id=request.user.id)
            if v:
                same_user = True
            else:
                same_user = False
            if v.upvote == 1 and v.downvote == 0:
                upvote = True
                downvote = False
            elif v.upvote == 0 and v.downvote == 1:
                upvote = False
                downvote = True
        except:
            same_user = False
        context = {"question": question,
                   "form": form,
                   "answers_list": answers_list,
                   "vote_count": vote_count,
                   "same_user": same_user,
                   "upvote": upvote,
                   "downvote": downvote
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
    is_upvoted = request.POST['is_upvoted']
    # print(type(is_upvoted))
    if is_upvoted == "1":
        v = Vote.objects.get(user_id=request.user.id, question_id=request.POST['question_id'])
        v.upvote = 0
        v.save()
    else:
        try:
            v = Vote.objects.get(user_id=request.user.id, question_id=request.POST['question_id'])
            if v.upvote == 0:
                v.upvote = 1
                v.save()
                return JsonResponse({'status': 'ok'})
        except:
            v = Vote(user_id=request.user.id, question_id=request.POST['question_id'], upvote=request.POST['upvote'], downvote=request.POST['downvote'])
            v.save()
    return JsonResponse({'status': 'ok'})


@login_required()
def downvote(request):
    pass