from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
import json
from .models import Task
from .serializers import TaskSerializer
from .tasks import process_task

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        cache_key = "task_list"
        cached_data = cache.get(cache_key)
        if cached_data:
            print("📦 從 Redis 快取取資料")
            return Response(json.loads(cached_data))
        print("📡 查詢資料庫")
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, json.dumps(serializer.data), timeout=60)
        return Response(serializer.data)

    def perform_create(self, serializer):
        instance = serializer.save()
        cache.delete("task_list")
        process_task.delay(instance.id)  # 非同步任務