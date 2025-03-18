from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Max
from django.db.models import Q

from datetime import datetime, timedelta

# Отправка почты
from django.core.mail import send_mail

# Подключение моделей
from .models import Category, Catalog, Client, Position, Employee, Sale, Application, Movement, News 
# Подключение форм
from .forms import CategoryForm, CatalogForm, ClientForm, PositionForm, EmployeeForm, SaleForm, ApplicationForm, MovementForm, NewsForm, SignUpForm

from django.db.models import Sum

from django.db import models

import sys

import math

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.db.models.query import QuerySet

import csv
import xlwt
from io import BytesIO

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

###################################################################################################

# Стартовая страница 
def index(request):
    try:
        news13 = News.objects.all().order_by('-daten')[0:4]
        return render(request, "index.html", {"news13": news13})            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

# Контакты
def contact(request):
    try:
        return render(request, "contact.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Сервисы
def service1(request):
    return render(request, "services/service1.html")
    # try:
    #     return render(request, "service/service1.html")
    # except Exception as exception:
    #     print(exception)
    #     return HttpResponse(exception)

def service2(request):
    try:
        return render(request, "services/service2.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

def service3(request):
    try:
        return render(request, "services/service3.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

def service4(request):
    try:
        return render(request, "services/service4.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

def service5(request):
    try:
        return render(request, "services/service5.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

def service6(request):
    try:
        return render(request, "services/service6.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

def service7(request):
    try:
        return render(request, "services/service7.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

def service8(request):
    try:
        return render(request, "services/service8.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

def service9(request):
    try:
        return render(request, "services/service9.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

###################################################################################################

# Отчеты
@login_required
@group_required("Employees", "Managers")
def report_index(request):
    try:
        catalog = Catalog.objects.all().order_by('category').order_by('title')
        if 'searchBtn' in request.POST:
            start_date = request.POST.get("start_date")
            fd = datetime.strptime(request.POST.get("finish_date"), '%Y-%m-%d') + timedelta(days=1)     # Дата с минутами
            #print(request.POST.get("finish_date"))
            #print(fd)
            finish_date = request.POST.get("finish_date")
            #  Проданый товар
            sale = Sale.objects.filter(dates__range=[start_date, fd.strftime('%Y-%m-%d')]).order_by('dates')
            sale_id= Sale.objects.filter(dates__range=[start_date, fd.strftime('%Y-%m-%d')]).only('catalog_id')
        else:
            start_date = (datetime.now()-timedelta(days=365)).strftime('%Y-%m-%d')
            finish_date = datetime.now().strftime('%Y-%m-%d')
            #  Проданый товар
            sale = Sale.objects.all().order_by('dates')
            sale_id= Sale.objects.all().only('catalog_id')
        # Итого
        total = Catalog.objects.filter(id__in = sale_id).aggregate(Sum('price'))              
        return render(request, "report/index.html", {"catalog": catalog, "sale": sale,  "total": total, "start_date": start_date, "finish_date": finish_date})        
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def category_index(request):
    try:
        category = Category.objects.all().order_by('title')
        return render(request, "category/index.html", {"category": category,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def category_create(request):
    try:
        if request.method == "POST":
            category = Category()
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/create.html", {"form": categoryform})
        else:        
            categoryform = CategoryForm()
            return render(request, "category/create.html", {"form": categoryform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def category_edit(request, id):
    try:
        category = Category.objects.get(id=id)
        if request.method == "POST":
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/edit.html", {"form": categoryform})
        else:
            # Загрузка начальных данных
            categoryform = CategoryForm(initial={'title': category.title, })
            return render(request, "category/edit.html", {"form": categoryform})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def category_delete(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return HttpResponseRedirect(reverse('category_index'))
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def category_read(request, id):
    try:
        category = Category.objects.get(id=id) 
        return render(request, "category/read.html", {"category": category})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

####################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def catalog_index(request):
    catalog = Catalog.objects.all().order_by('title')
    return render(request, "catalog/index.html", {"catalog": catalog})
    
# Список для просмотра и отправки в корзину
#@login_required
#@group_required("Managers")
#@login_required
def catalog_list(request):
    try:
        # Каталог доступных товаров
        catalog = Catalog.objects.all().order_by('category').order_by('title')
        # Категории и подкатегория товара (для поиска)
        category = Category.objects.all().order_by('title')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по категории товара
                selected_item_category = request.POST.get('item_category')
                #print(selected_item_category)
                if selected_item_category != '-----':
                    category_query = Category.objects.filter(title = selected_item_category).only('id').all()
                    catalog = catalog.filter(category_id__in = category_query).all()
                # Поиск по названию товара
                catalog_search = request.POST.get("catalog_search")
                #print(catalog_search)                
                if catalog_search != '':
                    catalog = catalog.filter(title__contains = catalog_search).all()
                # Сортировка
                sort = request.POST.get('radio_sort')
                #print(sort)
                direction = request.POST.get('checkbox_sort_desc')
                #print(direction)
                if sort=='title':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-title')
                    else:
                        catalog = catalog.order_by('title')
                elif sort=='price':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-price')
                    else:
                        catalog = catalog.order_by('price')
                elif sort=='category':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-category')
                    else:
                        catalog = catalog.order_by('category')
                return render(request, "catalog/list.html", {"catalog": catalog, "category": category, "selected_item_category": selected_item_category, "catalog_search": catalog_search, "sort": sort, "direction": direction,})    
            else:          
                return render(request, "catalog/list.html", {"catalog": catalog, "category": category,})    
        else:
            return render(request, "catalog/list.html", {"catalog": catalog, "category": category, })            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def catalog_create(request):
    try:
        if request.method == "POST":
            catalog = Catalog()
            catalog.category = Category.objects.filter(id=request.POST.get("category")).first()
            catalog.code = request.POST.get("code")
            catalog.title = request.POST.get("title")
            catalog.details = request.POST.get("details")        
            catalog.price = request.POST.get("price")
            catalogform = CatalogForm(request.POST)
            if catalogform.is_valid():
                catalog.save()
                return HttpResponseRedirect(reverse('catalog_index'))
            else:
                return render(request, "catalog/create.html", {"form": catalogform})
        else:        
            catalogform = CatalogForm()
            return render(request, "catalog/create.html", {"form": catalogform, })
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def catalog_edit(request, id):
    try:
        catalog = Catalog.objects.get(id=id) 
        if request.method == "POST":
            catalog.category = Category.objects.filter(id=request.POST.get("category")).first()
            catalog.code = request.POST.get("code")
            catalog.title = request.POST.get("title")
            catalog.details = request.POST.get("details")        
            catalog.price = request.POST.get("price")
            catalogform = CatalogForm(request.POST)
            if catalogform.is_valid():
                catalog.save()
                return HttpResponseRedirect(reverse('catalog_index'))
            else:
                return render(request, "catalog/edit.html", {"form": catalogform})            
        else:
            # Загрузка начальных данных
            catalogform = CatalogForm(initial={'category': catalog.category, 'code': catalog.code, 'title': catalog.title, 'details': catalog.details, 'price': catalog.price })
            #print('->',catalog.photo )
            return render(request, "catalog/edit.html", {"form": catalogform})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def catalog_delete(request, id):
    try:
        catalog = Catalog.objects.get(id=id)
        catalog.delete()
        return HttpResponseRedirect(reverse('catalog_index'))
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для менеджера.
@login_required
@group_required("Managers")
def catalog_read(request, id):
    try:
        catalog = Catalog.objects.get(id=id) 
        return render(request, "catalog/read.html", {"catalog": catalog})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для клиента
#@login_required
def catalog_details(request, id):
    try:
        # Товар с каталога
        catalog = Catalog.objects.get(id=id)
        # Отзывы на данный товар
        #reviews = ViewSale.objects.filter(catalog_id=id).exclude(rating=None)
        return render(request, "catalog/details.html", {"catalog": catalog,})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def client_index(request):
    try:
        client = Client.objects.all().order_by('name')
        return render(request, "client/index.html", {"client": client,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def client_create(request):
    try:
        if request.method == "POST":
            client = Client()
            client.name = request.POST.get("name")
            client.phone = request.POST.get("phone")
            client.leader = request.POST.get("leader")
            clientform = ClientForm(request.POST)
            if clientform.is_valid():
                client.save()
                return HttpResponseRedirect(reverse('client_index'))
            else:
                return render(request, "client/create.html", {"form": clientform})
        else:        
            clientform = ClientForm()
            return render(request, "client/create.html", {"form": clientform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def client_edit(request, id):
    try:
        client = Client.objects.get(id=id)
        if request.method == "POST":
            client.name = request.POST.get("name")
            client.phone = request.POST.get("phone")
            client.leader = request.POST.get("leader")
            clientform = ClientForm(request.POST)
            if clientform.is_valid():
                client.save()
                return HttpResponseRedirect(reverse('client_index'))
            else:
                return render(request, "client/edit.html", {"form": clientform})
        else:
            # Загрузка начальных данных
            clientform = ClientForm(initial={'name': client.name, 'phone': client.phone, 'leader': client.leader, })
            return render(request, "client/edit.html", {"form": clientform})
    except Client.DoesNotExist:
        return HttpResponseNotFound("<h2>Client not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def client_delete(request, id):
    try:
        client = Client.objects.get(id=id)
        client.delete()
        return HttpResponseRedirect(reverse('client_index'))
    except Client.DoesNotExist:
        return HttpResponseNotFound("<h2>Client not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def client_read(request, id):
    try:
        client = Client.objects.get(id=id) 
        return render(request, "client/read.html", {"client": client})
    except Client.DoesNotExist:
        return HttpResponseNotFound("<h2>Client not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def position_index(request):
    try:
        position = Position.objects.all().order_by('title')
        return render(request, "position/index.html", {"position": position,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def position_create(request):
    try:
        if request.method == "POST":
            position = Position()
            position.title = request.POST.get("title")
            positionform = PositionForm(request.POST)
            if positionform.is_valid():
                position.save()
                return HttpResponseRedirect(reverse('position_index'))
            else:
                return render(request, "position/create.html", {"form": positionform})
        else:        
            positionform = PositionForm()
            return render(request, "position/create.html", {"form": positionform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def position_edit(request, id):
    try:
        position = Position.objects.get(id=id)
        if request.method == "POST":
            position.title = request.POST.get("title")
            positionform = PositionForm(request.POST)
            if positionform.is_valid():
                position.save()
                return HttpResponseRedirect(reverse('position_index'))
            else:
                return render(request, "position/edit.html", {"form": positionform})
        else:
            # Загрузка начальных данных
            positionform = PositionForm(initial={'title': position.title, })
            return render(request, "position/edit.html", {"form": positionform})
    except Position.DoesNotExist:
        return HttpResponseNotFound("<h2>Position not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def position_delete(request, id):
    try:
        position = Position.objects.get(id=id)
        position.delete()
        return HttpResponseRedirect(reverse('position_index'))
    except Position.DoesNotExist:
        return HttpResponseNotFound("<h2>Position not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def position_read(request, id):
    try:
        position = Position.objects.get(id=id) 
        return render(request, "position/read.html", {"position": position})
    except Position.DoesNotExist:
        return HttpResponseNotFound("<h2>Position not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def employee_index(request):
    try:
        employee = Employee.objects.all().order_by('full_name')
        return render(request, "employee/index.html", {"employee": employee,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def employee_create(request):
    try:
        if request.method == "POST":
            employee = Employee()
            employee.full_name = request.POST.get("full_name")
            employee.position = Position.objects.filter(id=request.POST.get("position")).first()
            employee.phone = request.POST.get("phone")
            employeeform = EmployeeForm(request.POST)
            if employeeform.is_valid():
                employee.save()
                return HttpResponseRedirect(reverse('employee_index'))
            else:
                return render(request, "employee/create.html", {"form": employeeform})
        else:        
            employeeform = EmployeeForm()
            return render(request, "employee/create.html", {"form": employeeform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def employee_edit(request, id):
    try:
        employee = Employee.objects.get(id=id)
        if request.method == "POST":
            employee.full_name = request.POST.get("full_name")
            employee.position = Position.objects.filter(id=request.POST.get("position")).first()
            employee.phone = request.POST.get("phone")
            employeeform = EmployeeForm(request.POST)
            if employeeform.is_valid():
                employee.save()
                return HttpResponseRedirect(reverse('employee_index'))
            else:
                return render(request, "employee/edit.html", {"form": employeeform})
        else:
            # Загрузка начальных данных
            employeeform = EmployeeForm(initial={'full_name': employee.full_name, 'position': employee.position, 'phone': employee.phone, })
            return render(request, "employee/edit.html", {"form": employeeform})
    except Employee.DoesNotExist:
        return HttpResponseNotFound("<h2>Employee not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def employee_delete(request, id):
    try:
        employee = Employee.objects.get(id=id)
        employee.delete()
        return HttpResponseRedirect(reverse('employee_index'))
    except Employee.DoesNotExist:
        return HttpResponseNotFound("<h2>Employee not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def employee_read(request, id):
    try:
        employee = Employee.objects.get(id=id) 
        return render(request, "employee/read.html", {"employee": employee})
    except Employee.DoesNotExist:
        return HttpResponseNotFound("<h2>Employee not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################
# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def sale_index(request):
    sale = Sale.objects.all().order_by('dates')
    return render(request, "sale/index.html", {"sale": sale})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def sale_create(request):
    try:
        if request.method == "POST":
            sale = Sale()
            sale.dates = request.POST.get("dates")
            sale.catalog =Catalog.objects.filter(id=request.POST.get("catalog")).first()
            sale.client = Client.objects.filter(id=request.POST.get("client")).first()
            sale.employee = Employee.objects.filter(id=request.POST.get("employee")).first()
            saleform = SaleForm(request.POST)
            if saleform.is_valid():
                sale.save()
                return HttpResponseRedirect(reverse('sale_index'))
            else:
                return render(request, "sale/create.html", {"form": saleform})
        else:        
            saleform = SaleForm(initial={'dates': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
            return render(request, "sale/create.html", {"form": saleform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def sale_edit(request, id):
    try:
        sale = Sale.objects.get(id=id) 
        if request.method == "POST":
            sale.dates = request.POST.get("dates")
            sale.catalog =Catalog.objects.filter(id=request.POST.get("catalog")).first()
            sale.client = Client.objects.filter(id=request.POST.get("client")).first()
            sale.employee = Employee.objects.filter(id=request.POST.get("employee")).first()
            saleform = SaleForm(request.POST)
            if saleform.is_valid():
                sale.save()
                return HttpResponseRedirect(reverse('sale_index'))
            else:
                return render(request, "sale/edit.html", {"form": saleform})            
        else:
            # Загрузка начальных данных
            saleform = SaleForm(initial={'dates': sale.dates.strftime('%Y-%m-%d %H:%M:%S'), 'catalog': sale.catalog, 'client': sale.client, 'employee': sale.employee, })
            #print('->',sale.photo )
            return render(request, "sale/edit.html", {"form": saleform})
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def sale_delete(request, id):
    try:
        sale = Sale.objects.get(id=id)
        sale.delete()
        return HttpResponseRedirect(reverse('sale_index'))
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для менеджера.
@login_required
@group_required("Managers")
def sale_read(request, id):
    try:
        sale = Sale.objects.get(id=id) 
        return render(request, "sale/read.html", {"sale": sale})
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def application_index(request):
    try:
        application = Application.objects.all().order_by('datea')
        return render(request, "application/index.html", {"application": application})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список 
@login_required
def application_list(request):
    try:
        #print(request.user.id)
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        application = Application.objects.filter(user_id=request.user.id).order_by('-datea')
        return render(request, "application/list.html", {"application": application, 'first_name': first_name, 'last_name': last_name, 'email': email})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
    
# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
#@group_required("Managers")
def application_create(request):
    try:
        if request.method == "POST":
            application = Application()
            application.title = request.POST.get("title")
            application.details = request.POST.get("details")
            application.user_id = request.user.id
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_list'))
            else:
                return render(request, "application/create.html", {"form": applicationform})
        else:        
            applicationform = ApplicationForm()
            return render(request, "application/create.html", {"form": applicationform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def application_edit(request, id):
    try:
        application = Application.objects.get(id=id) 
        if request.method == "POST":
            application.title = request.POST.get("title")
            application.details = request.POST.get("details")
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_index'))
            else:
                return render(request, "application/edit.html", {"form": applicationform})
        else:
            # Загрузка начальных данных
            applicationform = ApplicationForm(initial={'title': application.title, 'details': application.details, })
            return render(request, "application/edit.html", {"form": applicationform})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def application_delete(request, id):
    try:
        application = Application.objects.get(id=id)
        application.delete()
        return HttpResponseRedirect(reverse('application_index'))
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def application_read(request, id):
    try:
        application = Application.objects.get(id=id)
        movement = Movement.objects.filter(application_id=id).order_by('-datem')
        return render(request, "application/read.html", {"application": application, "movement": movement})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def movement_index(request, application_id):
    try:
        movement = Movement.objects.filter(application_id=application_id).order_by('-datem')
        app = Application.objects.get(id=application_id)
        #movement = Movement.objects.all().order_by('-orders', '-datem')
        return render(request, "movement/index.html", {"movement": movement, "application_id": application_id, "app": app})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def movement_create(request, application_id):
    try:
        app = Application.objects.get(id=application_id)
        if request.method == "POST":
            movement = Movement()
            movement.application_id = application_id
            movement.datem = datetime.now()
            movement.status = request.POST.get("status")
            movement.details = request.POST.get("details")
            movementform = MovementForm(request.POST)
            if movementform.is_valid():
                movement.save()
                return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
            else:
                return render(request, "application/create.html", {"form": movementform})
        else:
            movementform = MovementForm(initial={ 'datem': datetime.now().strftime('%Y-%m-%d')})
            return render(request, "movement/create.html", {"form": movementform, "application_id": application_id, "app": app})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def movement_edit(request, id, application_id):
    app = Application.objects.get(id=application_id)
    try:
        movement = Movement.objects.get(id=id) 
        if request.method == "POST":
            #movement.datem = datetime.now()
            movement.status = request.POST.get("status")
            movement.details = request.POST.get("details")
            movementform = MovementForm(request.POST)
            if movementform.is_valid():
                movement.save()
                return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
            else:
                return render(request, "application/edit.html", {"form": movementform})
        else:
            # Загрузка начальных данных
            movementform = MovementForm(initial={'application': movement.application, 'datem': movement.datem.strftime('%Y-%m-%d'), 'status': movement.status, 'details': movement.details,  })
            return render(request, "movement/edit.html", {"form": movementform, "application_id": application_id, "app": app})
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def movement_delete(request, id, application_id):
    try:
        movement = Movement.objects.get(id=id)
        movement.delete()
        return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def movement_read(request, id, application_id):
    try:
        movement = Movement.objects.get(id=id) 
        return render(request, "movement/read.html", {"movement": movement, "application_id": application_id})
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    try:
        news = News.objects.all().order_by('-daten')
        return render(request, "news/index.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
def news_list(request):
    try:
        news = News.objects.all().order_by('-daten')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по названию 
                news_search = request.POST.get("news_search")
                #print(news_search)                
                if news_search != '':
                    news = news.filter(Q(title__contains = news_search) | Q(details__contains = news_search)).all()                
                return render(request, "news/list.html", {"news": news, "news_search": news_search, })    
            else:          
                return render(request, "news/list.html", {"news": news})                 
        else:
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
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/create.html", {"form": newsform})
        else:        
            newsform = NewsForm(initial={'daten': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
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
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/edit.html", {"form": newsform})
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d %H:%M:%S'), 'title': news.title, 'details': news.details, 'photo': news.photo })
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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

# Выход
from django.contrib.auth import logout
def logoutUser(request):
    logout(request)
    return render(request, "index.html")
