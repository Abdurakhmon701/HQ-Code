from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductSerializer, LessonSerializer, LessonProgressSerializer
from .models import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_lessons(request, pk):
    product = ProductModel.objects.get(pk=pk)
    lessons = LessonModel.objects.filter(products=product)
    lesson_progresses = LessonProgress.objects.filter(user=request.user, lesson__in=lessons)
    serializer = LessonProgressSerializer(lesson_progresses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_stats(request):
    products = ProductModel.objects.all()
    stats = []
    for product in products:
        lesson_progresses = LessonProgressModel.objects.filter(lesson__in=product.lesson_set.all())
        total_watched_time = lesson_progresses.aggregate(models.Sum('watched_time'))['watched_time__sum'] or 0
        total_completed_lessons = lesson_progresses.filter(is_completed=True).count()
        total_users = User.objects.filter(product=product).count()
        product_stats = {
            'product': ProductSerializer(product).data,
            'total_watched_time': total_watched_time,
            'total_completed_lessons': total_completed_lessons,
            'total_users': total_users,
            'purchase_percent': round((product.access_set.count() / User.objects.count()) * 100, 2)
        }
        stats.append(product_stats)
    return Response(stats)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lesson_detail(request, pk):
    lesson = LessonModel.objects.get(pk=pk)
    lesson_progress, created = LessonProgressModel.objects.get_or_create(user=request.user, lesson=lesson)
    serializer = LessonProgressSerializer(lesson_progress)
    return Response(serializer.data)
