from django.db import models

from django.contrib.auth.models import User


class ProductModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class LessonModel(models.Model):
    name = models.CharField(max_length=255, db_column='name')
    video_url = models.URLField(db_column='video_url')
    duration = models.PositiveIntegerField() # в секундах
    products = models.ManyToManyField(ProductModel)


class LessonProgressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    lesson = models.ForeignKey(LessonModel, on_delete=models.CASCADE, db_column='lesson')
    watched_time = models.PositiveIntegerField(default=0, db_column='watched_time') # в секундах
    is_completed = models.BooleanField(default=False, db_column='is_completed')

    # Функция, которая сохраняет при просмотре 80% видеоурока
    def save(self, *args, **kwargs):
        if self.watched_time >= 0.8 * self.lesson.duration:
            self.is_completed = True
        else:
            self.is_completed = False
        super().save(*args, **kwargs)