from django.shortcuts import render

from django.http import HttpResponse


def showMain(request):
    context = {'latest_question_list': 'something'}
    return render(request, 'HomePage/HomePage.html', context)