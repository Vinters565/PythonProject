from django.shortcuts import render

def index(request):
    return render(request, 'GamingProfession/index.html')


def demand(request):
    return render(request, 'GamingProfession/demand.html')


def geography(request):
    return render(request, 'GamingProfession/geography.html')


def skills(request):
    return render(request, 'GamingProfession/skills.html')


def latest_vacancies(request):
    return render(request, 'GamingProfession/latest_vacancies.html')
