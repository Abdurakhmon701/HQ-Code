from django.contrib import admin
from django.urls import path

from training_system.views import product_lessons, product_stats, lesson_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/<int:pk>/lessons/', product_lessons, name='product_lessons'),
    path('product/stats/', product_stats, name='product_stats'),
    path('lesson/<int:pk>/', lesson_detail, name='lesson_detail'),
]