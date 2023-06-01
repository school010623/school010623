from django.contrib import admin

# Register your models here.
from .models import Answers, Reviews, News

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Answers)
admin.site.register(Reviews)
admin.site.register(News)
