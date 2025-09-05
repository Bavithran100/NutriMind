from django.db import models
from django.contrib.auth.models import User

class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    mood = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 scale
    sleep_hours = models.FloatField()
    exercise_minutes = models.IntegerField()
    food = models.TextField()

    class Meta:
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"
