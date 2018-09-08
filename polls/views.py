from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Choice, Question
from .forms import *


"""
def index(request):
    return HttpResponse("Hello, world!")
"""

def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

"""
def detail(request, question_id):
    context = {'question_id': question_id}
    return render(request, 'polls/detail.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    choice_list = question.choice_set.all()
    context = {'question': question, 'choice_list':choice_list}
    return render(request, 'polls/detail.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = VoteForm(request.POST, question=question)
        if form.is_valid():
            form.save()
            return redirect('polls:results', question_id=question.id)
    else:
        form = VoteForm(question=question)

    context = {'question':question, 'form':form}
    return render(request, "polls/detail.html", context)
"""

@login_required
def detail(request, question_id):
    user = request.user
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = VoteForm(request.POST, question=question)
        if form.is_valid():
            form.save()
            return redirect('polls:results', question_id=question.id)
    else:
        form = VoteForm(question=question)

    context = {'user':user, 'question':question, 'form':form}
    return render(request, "polls/detail.html", context)

"""
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
"""

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:index')
    else:
        form = SignUpForm()

    context = {'form':form}
    return render(request, 'polls/signup.html', context)
