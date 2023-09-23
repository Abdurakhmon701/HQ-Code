from rest_framework import serializers
from .models import ProductModel, LessonModel, LessonProgressModel


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonModel
        fields = '__all__'


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_name = serializers.CharField(source='lesson.name')
    watched_percent = serializers.SerializerMethodField()

    class Meta:
        model = LessonProgressModel
        fields = ('lesson', 'lesson_name', 'watched_time', 'is_completed', 'watched_percent')

    def get_watched_percent(self, obj):
        return round((obj.watched_time / obj.lesson.duration) * 100, 2)