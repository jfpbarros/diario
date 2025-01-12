from django.contrib import admin
from .models import Pessoa, Diario,Tag
# Register your models here.

admin.site.register(Pessoa)
admin.site.register(Diario)
admin.site.register(Tag)
