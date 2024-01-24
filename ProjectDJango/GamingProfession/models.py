from django.db import models

class YearStatistic(models.Model):
    year = models.IntegerField(verbose_name='Год')
    salary_by_years = models.IntegerField(verbose_name='Динамика зарплат')
    salary_by_years_profession = models.IntegerField(verbose_name='Динамика зарплат для профессии')
    number_vac_by_years = models.IntegerField(verbose_name='Динамика кол-ва вакансий')
    number_profession_by_years = models.IntegerField(verbose_name='Динамика кол-ва вакансий для профессии')
    charts_years = models.ImageField(upload_to='charts', blank=True, verbose_name='График стат-ки по годам')

    class Meta:
        verbose_name = 'Статистика по годам'
        verbose_name_plural = 'Статистика по годам'


class CityStatistic(models.Model):
    city_salary = models.CharField(max_length=255, verbose_name='Город-зарплата')
    salary_by_city = models.IntegerField(verbose_name='Уровень зарплат по городам')
    city_percentage = models.CharField(max_length=255, verbose_name='Город-доля вакансий')
    percentage_by_city = models.FloatField(verbose_name='Доля вакансий по городам')
    charts_city = models.ImageField(upload_to='charts', blank=True, verbose_name='График стат-ки по годам')

    class Meta:
        verbose_name = 'Статистика по городам'
        verbose_name_plural = 'Статистика по городам'


class SkillsStatistic(models.Model):
    year_skills = models.CharField(max_length=255, verbose_name='Год')
    key_skills = models.TextField(verbose_name='Топ-20 навыков по годам')
    skills_count = models.TextField(verbose_name='Частотность навыков')
    charts_skills = models.ImageField(upload_to='charts', blank=True, verbose_name='Графики стат-ки по навыкам')
    class Meta:
        verbose_name = 'ТОП-20 навыков по годам'
        verbose_name_plural = 'ТОП-20 навыков по годам'
