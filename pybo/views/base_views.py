from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question, Answer

def index(request):
    """
    pybo 목록 출력
    """
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo content
    """

    question = get_object_or_404(Question, pk=question_id)

    page = request.GET.get('page','1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recommend')

    if so == 'recommend':
        answer_list = Answer.objects.filter(question=question).annotate(num_voter=Count('voter')).order_by('-num_voter',
                                                                                                           '-create_date')
    elif so == 'recent':
        answer_list = Answer.objects.filter(question=question).order_by('-create_date')

    if kw:
        answer_list = answer_list.filter(
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(answer_list, 3)
    page_obj = paginator.get_page(page)

    context = {'question': question, 'answer_list':page_obj,'page':page, 'kw':kw, 'so':so}

    return render(request, 'pybo/question_detail.html', context)


