from django.contrib import admin

# Register your models here.
from .models import Answers, Reviews, News

# ���������� ������ �� ������� �������� ���������� ��������������
admin.site.register(Answers)
admin.site.register(Reviews)
admin.site.register(News)
