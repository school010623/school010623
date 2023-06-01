from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.urls import reverse

from django.contrib.auth import login as auth_login

import datetime

import time

import csv
import xlwt
from io import BytesIO

# Подключение моделей
from django.contrib.auth.models import User, Group

from django.db import models
from django.db.models import Q

from .models import Answers, Reviews, News
# Подключение форм
from .forms import AnswersFormCreate, AnswersFormEdit, ReviewsForm, NewsForm, SignUpForm

from django.contrib.auth.models import AnonymousUser

# Create your views here.

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

# Стартовая страница 
def index(request):
    news1 = News.objects.all().order_by('-daten')[0:1]
    news24 = News.objects.all().order_by('-daten')[1:4]
    reviews14 = Reviews.objects.all().order_by('?')[0:4]
    return render(request, "index.html", {"news1": news1, "news24": news24, "reviews14": reviews14, })    

# Контакты
def contact(request):
    return render(request, "contact.html")

# Кабинет
@login_required
def cabinet(request):
    reviews = Reviews.objects.filter(user_id=request.user.id).order_by('-dater')    
    return render(request, "cabinet.html", { "reviews": reviews, })# Кабинет

# Администрация
def administration(request):
    return render(request, "administration.html")

# Первый класс
def first(request):
    return render(request, "first.html")

# Школьная форма
def uniform(request):
    return render(request, "uniform.html")

# Учебники
def manual(request):
    return render(request, "manual.html")

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def answers_index(request):
    answers = Answers.objects.all().order_by('-datea')
    return render(request, "answers/index.html", {"answers": answers})

# Список для просмотра
def answers_list(request):
    answers = Answers.objects.all().order_by('-datea')
    return render(request, "answers/list.html", {"answers": answers})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
def answers_create(request):
    if request.method == "POST":
        # Текущий пользователь
        _user_id = request.user.id
        answers = Answers()        
        answers.datea = datetime.datetime.now()
        answers.question = request.POST.get("question")
        answers.user_id = _user_id
        answers.save()
        return HttpResponseRedirect(reverse('answers_list'))
    else:        
        answersform = AnswersFormCreate(request.FILES)
        return render(request, "answers/create.html", {"form": answersform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
# И вначале по этому идентификатору мы пытаемся найти объект с помощью метода Answers.objects.get(id=id).
# Поскольку в случае отсутствия объекта мы можем столкнуться с исключением Answers.DoesNotExist,
# то соответственно нам надо обработать подобное исключение, если вдруг будет передан несуществующий идентификатор.
# И если объект не будет найден, то пользователю возващается ошибка 404 через вызов return HttpResponseNotFound().
# Если объект найден, то обработка делится на две ветви.
# Если запрос POST, то есть если пользователь отправил новые изменненые данные для объекта, то сохраняем эти данные в бд и выполняем переадресацию на корень веб-сайта.
# Если запрос GET, то отображаем пользователю страницу edit.html с формой для редактирования объекта.
@login_required
@group_required("Managers")
def answers_edit(request, id):
    try:
        # Текущий пользователь
        _user_id = request.user.id
        
        answers = Answers.objects.get(id=id) 
        if request.method == "POST":
            answers.datea = request.POST.get("datea")
            answers.answer = request.POST.get("answer")
            answers.specialist_id = _user_id
            answers.save()
            return HttpResponseRedirect(reverse('answers_index'))
        else:
            # Загрузка начальных данных
            print(answers.specialist)
            if answers.specialist is None:                
                answersform = AnswersFormEdit(initial={'datea': answers.datea.strftime('%Y-%m-%d'), 'question': answers.question, 'answer': answers.answer, 'user': answers.user.username, 'specialist': answers.specialist })
            else:
                answersform = AnswersFormEdit(initial={'datea': answers.datea.strftime('%Y-%m-%d'), 'question': answers.question, 'answer': answers.answer, 'user': answers.user.username, 'specialist': answers.specialist.username  })
            return render(request, "answers/edit.html", {"form": answersform})
    except Answers.DoesNotExist:
        return HttpResponseNotFound("<h2>Answers not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def answers_delete(request, id):
    try:
        answers = Answers.objects.get(id=id)
        answers.delete()
        return HttpResponseRedirect(reverse('answers_index'))
    except Answers.DoesNotExist:
        return HttpResponseNotFound("<h2>Answers not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def answers_read(request, id):
    try:
        answers = Answers.objects.get(id=id) 
        return render(request, "answers/read.html", {"answers": answers})
    except Answers.DoesNotExist:
        return HttpResponseNotFound("<h2>Answers not found</h2>")

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def reviews_index(request):
    reviews = Reviews.objects.all().order_by('dater')
    return render(request, "reviews/index.html", {"reviews": reviews})

# Список для просмотра
def reviews_list(request):
    reviews = Reviews.objects.all().order_by('dater')
    return render(request, "reviews/list.html", {"reviews": reviews})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
def reviews_create(request):
    if request.method == "POST":
        # Текущий пользователь
        _user_id = request.user.id
        reviews = Reviews()        
        reviews.dater =  datetime.datetime.now()
        reviews.details = request.POST.get("details")
        reviews.user_id = _user_id
        reviews.save()
        return HttpResponseRedirect(reverse('reviews_list'))
    else:        
        reviewsform = ReviewsForm(request.FILES)
        return render(request, "reviews/create.html", {"form": reviewsform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
# И вначале по этому идентификатору мы пытаемся найти объект с помощью метода Reviews.objects.get(id=id).
# Поскольку в случае отсутствия объекта мы можем столкнуться с исключением Reviews.DoesNotExist,
# то соответственно нам надо обработать подобное исключение, если вдруг будет передан несуществующий идентификатор.
# И если объект не будет найден, то пользователю возващается ошибка 404 через вызов return HttpResponseNotFound().
# Если объект найден, то обработка делится на две ветви.
# Если запрос POST, то есть если пользователь отправил новые изменненые данные для объекта, то сохраняем эти данные в бд и выполняем переадресацию на корень веб-сайта.
# Если запрос GET, то отображаем пользователю страницу edit.html с формой для редактирования объекта.
@login_required
@group_required("Managers")
def reviews_edit(request, id):
    try:
        # Текущий пользователь
        _user_id = request.user.id
        
        reviews = Reviews.objects.get(id=id) 
        if request.method == "POST":
            reviews.dater = request.POST.get("dater")
            reviews.details = request.POST.get("details")
            reviews.user_id = _user_id
            reviews.save()
            return HttpResponseRedirect(reverse('reviews_index'))
        else:
            # Загрузка начальных данных
            reviewsform = ReviewsForm(initial={'dater': reviews.dater.strftime('%Y-%m-%d'), 'details': reviews.details, 'user': reviews.user  })
            return render(request, "reviews/edit.html", {"form": reviewsform})
    except Reviews.DoesNotExist:
        return HttpResponseNotFound("<h2>Reviews not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def reviews_delete(request, id):
    try:
        reviews = Reviews.objects.get(id=id)
        reviews.delete()
        return HttpResponseRedirect(reverse('reviews_index'))
    except Reviews.DoesNotExist:
        return HttpResponseNotFound("<h2>Reviews not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def reviews_read(request, id):
    try:
        reviews = Reviews.objects.get(id=id) 
        return render(request, "reviews/read.html", {"reviews": reviews})
    except Reviews.DoesNotExist:
        return HttpResponseNotFound("<h2>Reviews not found</h2>")

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    try:
        #news = News.objects.all().order_by('surname', 'name', 'patronymic')
        #return render(request, "news/index.html", {"news": news})
        news = News.objects.all().order_by('-daten')
        return render(request, "news/index.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)


# Список для просмотра
def news_list(request):
    try:
        news = News.objects.all().order_by('-daten')
        return render(request, "news/list.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    try:
        if request.method == "POST":
            news = News()        
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                news.photo = request.FILES['photo']        
            news.save()
            return HttpResponseRedirect(reverse('news_index'))
        else:        
            #newsform = NewsForm(request.FILES, initial={'daten': datetime.datetime.now().strftime('%Y-%m-%d'),})
            newsform = NewsForm(initial={'daten': datetime.datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "news/create.html", {"form": newsform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            news.save()
            return HttpResponseRedirect(reverse('news_index'))
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d'), 'title': news.title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Регистрационная форма 
def signup(request):
    try:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return HttpResponseRedirect(reverse('index'))
                #return render(request, 'registration/register_done.html', {'new_user': user})
        else:
            form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    try:
        model = User
        fields = ('first_name', 'last_name', 'email',)
        template_name = 'registration/my_account.html'
        success_url = reverse_lazy('index')
        #success_url = reverse_lazy('my_account')
        def get_object(self):
            return self.request.user
    except Exception as exception:
        print(exception)




