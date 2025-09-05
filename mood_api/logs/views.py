from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from .models import DailyLog
from .serializers import DailyLogSerializer

class DailyLogViewSet(viewsets.ModelViewSet):
    serializer_class = DailyLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def weekly_report(self, request):
        # Get last 7 days logs
        from datetime import datetime, timedelta
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=6)

        logs = self.get_queryset().filter(date__range=[start_date, end_date])

        report = logs.aggregate(
            avg_mood=Avg('mood'),
            avg_sleep=Avg('sleep_hours'),
            avg_exercise=Avg('exercise_minutes')
        )

        # Get mood data for chart
        mood_data = []
        for i in range(7):
            date = start_date + timedelta(days=i)
            log = logs.filter(date=date).first()
            mood_data.append(log.mood if log else None)

        return Response({
            'start_date': start_date,
            'end_date': end_date,
            'average_mood': report['avg_mood'] or 0,
            'average_sleep': report['avg_sleep'] or 0,
            'average_exercise': report['avg_exercise'] or 0,
            'logs_count': logs.count(),
            'mood_trend': mood_data
        })
