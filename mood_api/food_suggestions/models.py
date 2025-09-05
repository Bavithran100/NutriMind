from django.db import models

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # e.g., breakfast, lunch, dinner
    calories = models.IntegerField()
    protein = models.FloatField()  # grams
    carbs = models.FloatField()  # grams
    fat = models.FloatField()  # grams
    mood_boost = models.IntegerField(default=0)  # 1-5 scale for mood impact

    def __str__(self):
        return self.name
