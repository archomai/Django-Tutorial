from unittest import loader

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

from polls.models import Question, Choice


def index(request):
    # 가장 최근에 발핸된 최대 4개의 Question목록
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }

    # render를 사용
    return render(request, 'polls/index.html', context)

    # template 을 명시적으로 불러와 rendering
    # template = loader.get_template('poll/index.html')
    # return HttpResponse(template.render(context, request))

    #쉼표단위로 구분된 Question목록의 각 항목의 question_text로 만들어진 문자열
    # output = ', '.join([q.question_text for q in latest_question_list])


def detail(request, question_id):
    """
    question_id에 해당하는 Question객체를 템플릿에 전달
        key: 'question'
        template: polls/templates/polls/detail.html
    템플릿에서는
    1. 전달받은 question의 question_text를 출력
        {{ question.question_text }}
    2. question이 가진 모든 Choice들을 ul > li로 출력
        {% for choice in question.choice_set.all %}
    :param request:
    :param question_id:
    :return:
    """
    # try:
    #     # question을 get()시도
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     # DoesNotExist예외가 발생 시
    #     # Http404 페이지가 보임
    #     raise Http404('Question does not exist')

    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
    }

    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    response = "You're looking at teh results of questions %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    """
    1. request.POST에 choice에 온 value를
        pk로 갖는 Choice객체의
        votes값을 1 증가시키고
        DB에 저장
    2. 이후 question_id에 해당하는 results뷰로 redirect

    :param request:
    :param question_id:
    :return:
    """
    # request.POST의 name(choice)에 온 value를
    choice_pk = request.POST['choice']
    # pk로 가지는 Choice객체 choice
    choice = Choice.objects.get(pk=choice_pk)
    # choice의 votes값을 1 증가시키고
    choice.votes += 1
    # DB에 저장
    choice.save()

    # 이후 question_id인자값을 전달하며
    # polls:results로 redirect
    return redirect(
        'polls:results',
        question_id=question_id
    )
