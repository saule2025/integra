from django.contrib import admin

from .models import Category, Catalog, Client, Position, Employee, Sale, Application, Movement, News 

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Category)
admin.site.register(Catalog)
admin.site.register(Client)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(Sale)
admin.site.register(Application)
admin.site.register(Movement)
admin.site.register(News)

