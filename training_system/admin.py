from django.contrib import admin
from .models import *

admin.site.register(ProductModel)
admin.site.register(LessonModel)
admin.site.register(LessonProgressModel)
