import numpy as np
from django.shortcuts import render
from django.template.defaulttags import register
from .models import *
from datetime import datetime, timedelta, timezone
import pandas as pd
from aiohttp import ClientSession
import asyncio
from .forms import AddDateForm

def index(request):
    return render(request, 'GamingProfession/index.html')


def demand(request):
    year_statistic = YearStatistic.objects.all()
    context = {
        'year_statistic': year_statistic,
    }
    return render(request, 'GamingProfession/demand.html', context=context)


def geography(request):
    city_statistic = CityStatistic.objects.all()
    context = {
        'city_statistic': city_statistic,
    }
    return render(request, 'GamingProfession/geography.html', context=context)


def skills(request):
    skills_statistic = SkillsStatistic.objects.all()
    key_skills = {row.year_skills: row.key_skills.split(';') for row in skills_statistic}
    skills_count = {row.year_skills: row.skills_count.split(';') for row in skills_statistic}
    years = [row.year_skills for row in skills_statistic]
    context = {
        'key_skills': key_skills,
        'skills_count': skills_count,
        'years': years,
        'skills_statistic': skills_statistic
    }
    return render(request, 'GamingProfession/skills.html', context=context)


def latest_vacancies(request):
    all_vacancies = None
    date = ''
    now = datetime.now(timezone.utc) + timedelta(hours=3, minutes=0)
    if request.method == 'POST':
        forms = AddDateForm(request.POST)
        if forms.is_valid():
            if now.date() - timedelta(days=30) < forms.cleaned_data['date'] <= now.date():
                all_vacancies = GetVacancies().get_vacancies(forms.cleaned_data['date'])
                date = f"за {forms.cleaned_data['date']}"
            else:
                forms.add_error('date',
                                f'Указанная дата должна находиться в промежутке с {(now.date() - timedelta(days=30)).strftime("%d.%m.%Y")} числа до сегодняшнего дня')
                date = ''
    else:
        forms = AddDateForm()
        date = ''

    context = {
        'vacancies': all_vacancies,
        'date': date,
        'forms': forms
    }
    return render(request, 'GamingProfession/latest_vacancies.html', context)


@register.filter
def get_range(value):
    return range(value)


@register.filter
def get_value(value, key):
    return value[key]


@register.filter
def incr(value):
    return value + 1


@register.filter
def format_datetime(value):
    date = value.replace('T', '-').replace(':', '-').replace('+', '-')
    year, month, day, hour, minute, second, timezone = date.split('-')
    return f'{day}.{month}.{year} {hour}:{minute}:{second}'


@register.filter
def to_int(value):
    return int(value)


class GetVacancies:
    def get_vacancies(self, date=datetime.today().date(), count=10):
        vacancies = asyncio.run(self.__collect_suitable_vacancies(date, count))
        # vacancies.reset_index(inplace=True)
        return vacancies.to_dict('records')

    async def __collect_suitable_vacancies(self, date, count):
        tasks_vacancies_all_day = []
        for page in range(20):
            tasks_vacancies_all_day.append(asyncio.create_task(self.__get_page(date, page)))

        tasks_vacancies = []
        vacancies_all_day = await asyncio.gather(*tasks_vacancies_all_day)
        for vacancies_per_hour in vacancies_all_day:
            if vacancies_per_hour is None or len(vacancies_per_hour) == 0:
                continue
            for vacancy in vacancies_per_hour:
                tasks_vacancies.append(asyncio.create_task(self.__get_vacancy_info(self.__safe_get(vacancy, 'id'))))

        vacancy_list = []
        vacancies = await asyncio.gather(*tasks_vacancies)
        for vacancy in vacancies:
            if len(vacancy_list) == count:
                break
            vacancy_list.append({'name': self.__safe_get(vacancy, 'name'),
                                 'description': self.__safe_get(vacancy, 'description'),
                                 'key_skills': [skill['name'] for skill in
                                                self.__safe_get(vacancy, 'key_skills')],
                                 'salary_from': self.__safe_get(vacancy, 'salary', 'from'),
                                 'salary_to': self.__safe_get(vacancy, 'salary', 'to'),
                                 'salary_currency': self.__safe_get(vacancy, 'salary', 'currency'),
                                 'area_name': self.__safe_get(vacancy, 'area', 'name'),
                                 'published_at': self.__safe_get(vacancy, 'published_at'),
                                 'employer': self.__safe_get(vacancy, 'employer', 'name'),
                                 'employer_logo': self.__safe_get(vacancy, 'employer', 'logo_urls', '240'),
                                 'url': self.__safe_get(vacancy, 'alternate_url')})
        return pd.DataFrame(vacancy_list)

    @staticmethod
    async def __get_page(date, page):
        async with ClientSession(trust_env=True) as session:
            url = f'https://api.hh.ru/vacancies'
            params = {
                'page': page,
                'per_page': 100,
                'specialization': 1,
                'date_from': f'{date}T00:00:00',
                'date_to': f'{date}T23:59:00',
                'order_by': 'publication_time',
                'search_field': 'name',
                'text': 'GameDev OR game OR unity OR игр OR unreal',
            }
            async with session.get(url=url, params=params) as response:
                result_json = await response.json()
                if response.status == 426 or response.status == 400:
                    return None
                if 'errors' in result_json and result_json['errors'][0]['value'] == 'captcha_required':
                    print(f"{result_json['errors'][0]['captcha_url']}&backurl=http://127.0.0.1:5500/index.html")
                    return
                results = result_json['items']
                return results

    @staticmethod
    async def __get_vacancy_info(id_vac):
        async with ClientSession(trust_env=True) as session:
            url = f'https://api.hh.ru/vacancies/{id_vac}'
            async with session.get(url=url) as response:
                result_data = await response.json()
                if 'errors' in result_data and result_data['errors'][0]['value'] == 'captcha_required':
                    print(f"{result_data['errors'][0]['captcha_url']}&backurl=http://127.0.0.1:5500/index.html")
                    return
                results = result_data
                return results

    @staticmethod
    def __safe_get(vacancy, *keys):
        for key in keys:
            try:
                vacancy = vacancy[key]
            except:
                return np.NaN
        return vacancy