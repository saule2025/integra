from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Категория товара (услуги)
class Category(models.Model):
    title = models.CharField(_('category_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'category'
    def __str__(self):
        # Вывод названияв тег SELECT 
        return "{}".format(self.title)

# Каталог товаров (услуг)
class Catalog(models.Model):
    category = models.ForeignKey(Category, related_name='catalog_category', on_delete=models.CASCADE)
    code = models.CharField(_('catalog_code'), max_length=255)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('catalog_price'), max_digits=9, decimal_places=2)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'catalog'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{} {} {}".format(self.category, self.title, self.price)

# Клиенты
class Client(models.Model):
    name = models.CharField(_('client_name'), max_length=128)
    phone = models.CharField(_('client_phone'), max_length=32)
    leader = models.CharField(_('client_leader'), max_length=128)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'client'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['name']),
        ]
        # Сортировка по умолчанию
        ordering = ['name']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{}, {}".format(self.name, self.phone)

# Должность
class Position(models.Model):
    title = models.CharField(_('position_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'position'
    def __str__(self):
        # Вывод названияв тег SELECT 
        return "{}".format(self.title)

# Сотрудник 
class Employee(models.Model):
    full_name = models.CharField(_('full_name'), max_length=128)
    position = models.ForeignKey(Position, related_name='employee_position', on_delete=models.CASCADE)
    phone = models.CharField(_('phone'), max_length=64)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'employee'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['full_name']),
            models.Index(fields=['position']),
        ]
        # Сортировка по умолчанию
        ordering = ['full_name']
    def __str__(self):
        # Вывод в тег Select 
        return "{}, {}".format(self.full_name, self.position)

# Продажа 
class Sale(models.Model):
    dates = models.DateTimeField(_('dates'))
    catalog = models.ForeignKey(Catalog, related_name='sale_catalog', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='sale_client', on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, related_name='sale_employee', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'sale'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['catalog']),
            models.Index(fields=['client']),
            models.Index(fields=['employee']),
        ]
        # Сортировка по умолчанию
        ordering = ['dates']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{}: {}, {}".format(self.catalog, self.client, self.employee)
        # Таблицу не надо не добавлять не удалять
        #managed = False

# Заявка клиента
class Application(models.Model):
    datea = models.DateTimeField(_('datea'), auto_now_add=True)
    user = models.ForeignKey(User, related_name='application_user', on_delete=models.CASCADE)
    title = models.CharField(_('application_title'), max_length=255)
    details = models.TextField(_('application_details'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'application'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datea']),
            models.Index(fields=['user']),
        ]
        # Сортировка по умолчанию
        ordering = ['datea']
    def __str__(self):
        # Вывод в тег Select
        return "{} ({}): {}".format(self.datea.strftime('%d.%m.%Y'), self.user, self.title)

# Рассмотрение заявки клиента
class Movement(models.Model):
    application = models.ForeignKey(Application, related_name='movement_application', on_delete=models.CASCADE)
    datem = models.DateTimeField(_('datem'))
    status = models.CharField(_('movement_status'), max_length=128)
    details = models.TextField(_('movement_details'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'movement'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['datem']),
        ]
        # Сортировка по умолчанию
        ordering = ['datem']        
    def __str__(self):
        # Вывод в тег Select
        return "{} ({}): {}".format(self.datem.strftime('%d.%m.%Y'), self.application, self.status)

# Новости 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('news_title'), max_length=256)
    details = models.TextField(_('news_details'))
    photo = models.ImageField(_('news_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'news'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['daten']),
        ]
        # Сортировка по умолчанию
        ordering = ['daten']
