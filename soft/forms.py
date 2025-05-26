from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput, DateTimeInput
from .models import Category, Catalog, Client, Position, Employee, Sale, Application, Movement, News 
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import pytz

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

# Категория товара
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('category_title'),            
        }
    # Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data

# Товар (услуга)
class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ('category', 'code', 'title', 'details', 'price')
        widgets = {
            'category': forms.Select(attrs={'class': 'chosen'}),
            'code': TextInput(attrs={"size":"50"}),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 5}),            
            'price': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
        }
    # Метод-валидатор для поля price
    def clean_price(self):
        data = self.cleaned_data['price']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Price must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data       

# Клиенты
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'leader',]
        widgets = {
            'name': TextInput(attrs={"size":"100"}),            
            'phone': TextInput(attrs={"size":"50", "type":"tel"}),            
            'leader': TextInput(attrs={"size":"100"}),
        }

# Должность
class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('position_title'),            
        }

# Сотрудник
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'position', 'phone',]
        widgets = {
            'full_name': TextInput(attrs={"size":"100"}), 
            'position': forms.Select(attrs={'class': 'chosen'}),
            'phone': TextInput(attrs={"size":"50", "type":"tel"}),            
        }

# Продажа
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('dates', 'catalog', 'client', 'employee')
        widgets = {
            'dates': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'catalog': forms.Select(attrs={'class': 'chosen'}),
            'client': forms.Select(attrs={'class': 'chosen'}),
            'employee': forms.Select(attrs={'class': 'chosen'}),
        }
        labels = {
            'catalog': _('catalog_title'),            
            'client': _('client'),            
            'employee': _('employee'),            
        }

# Заявки
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('title', 'details')
        widgets = {
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),            
        }        

# Движение заявки
class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ('datem', 'status', 'details')
        widgets = {
            'datem': DateInput(attrs={"type":"date", "readonly":"readonly"}),
            'status': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),
        }

# Новости
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'title', 'details', 'photo')
        widgets = {
            'daten': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля daten
    def clean_daten(self):        
        if isinstance(self.cleaned_data['daten'], datetime.date) == True:
            data = self.cleaned_data['daten']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   

# Движение заявки
class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ('datem', 'status', 'details')
        widgets = {
            'datem': DateInput(attrs={"type":"date", "readonly":"readonly"}),
            'status': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),
        }

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
