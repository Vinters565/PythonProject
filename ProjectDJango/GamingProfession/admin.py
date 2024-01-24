from django.contrib import admin

from .models import *

class YearStatisticAdmin(admin.ModelAdmin):
    list_display = ('year', 'salary_by_years', 'salary_by_years_profession', 'number_vac_by_years', 'number_profession_by_years',
                    'charts_years')


class CityStatisticAdmin(admin.ModelAdmin):
    list_display = ('city_salary', 'salary_by_city', 'city_percentage', 'percentage_by_city', 'charts_city')


class SkillsStatisticAdmin(admin.ModelAdmin):
    list_display = ('year_skills', 'key_skills', 'skills_count', 'charts_skills')


admin.site.register(YearStatistic, YearStatisticAdmin)
admin.site.register(CityStatistic, CityStatisticAdmin)
admin.site.register(SkillsStatistic, SkillsStatisticAdmin)
