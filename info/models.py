from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from django.core.files.storage import default_storage as storage  

from django.contrib.auth.models import User

import math

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат пол¤ и поведение ваших данных.
# Обычно одна модель представл¤ет одну таблицу в базе данных.
# Кажда¤ модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представл¤ет поле в базе данных.
# Django предоставл¤ет автоматически созданное API дл¤ доступа к данным

# choices (список выбора). »тератор (например, список или кортеж) 2-х элементных кортежей,
# определ¤ющих варианты значений дл¤ пол¤.
# при определении, виджет формы использует select вместо стандартного текстового пол¤
# и ограничит значение пол¤ указанными значени¤ми.

# читабельное им¤ пол¤ (метка, label).  аждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необ¤зательное читабельное название.
# если оно не указано, Django самосто¤тельно создаст его, использу¤ название пол¤, замен¤¤ подчеркивание на пробел.
# null - ≈сли True, Django сохранит пустое значение как NULL в базе данных. ѕо умолчанию - False.
# blank - ≈сли True, поле не об¤зательно и может быть пустым. ѕо умолчанию - False.
# Ёто не то же что и null. null относитс¤ к базе данных, blank - к проверке данных.
# если поле содержит blank=True, форма позволит передать пустое значение.
# при blank=False - поле об¤зательно.

# Ответы на вопросы 
class Answers(models.Model):
    datea = models.DateTimeField(_('datea'))
    question = models.TextField(_('question'))
    answer = models.TextField(_('answer'), blank=True, null=True)
    user = models.ForeignKey(User, related_name='user_answers', on_delete=models.CASCADE)
    specialist = models.ForeignKey(User, blank=True, null=True, related_name='specialist_answers', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'answers'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datea']),
        ]
        # Сортировка по умолчанию
        ordering = ['datea']

# Отзывы 
class Reviews(models.Model):
    dater = models.DateTimeField(_('dater'))
    details = models.TextField(_('details_reviews'))
    user = models.ForeignKey(User, related_name='user_reviews', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'reviews'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['dater']),
        ]
        # Сортировка по умолчанию
        ordering = ['dater']

# Ќовости 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('title_news'), max_length=256)
    details = models.TextField(_('details_news'))
    photo = models.ImageField(_('photo_news'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # ѕараметры модели
        # ѕереопределение имени таблицы
        db_table = 'news'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['daten']),
        ]
        # —ортировка по умолчанию
        ordering = ['daten']
    #def save(self):
    #    super().save()
    #    img = Image.open(self.photo.path) # Open image
    #    # resize image
    #    if img.width > 512 or img.height > 700:
    #        proportion_w_h = img.width/img.height  # ќтношение ширины к высоте 
    #        output_size = (512, int(512/proportion_w_h))
    #        img.thumbnail(output_size) # »зменение размера
    #        img.save(self.photo.path) # —охранение

