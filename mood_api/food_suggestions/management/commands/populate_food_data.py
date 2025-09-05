from django.core.management.base import BaseCommand
from food_suggestions.models import FoodItem

class Command(BaseCommand):
    help = 'Populate database with sample food items'

    def handle(self, *args, **options):
        # Clear existing data
        FoodItem.objects.all().delete()

        # Sample food data
        food_data = [
            # Breakfast items
            {'name': 'Oats with Banana', 'category': 'breakfast', 'calories': 300, 'protein': 10, 'carbs': 50, 'fat': 8, 'mood_boost': 3},
            {'name': 'Greek Yogurt with Berries', 'category': 'breakfast', 'calories': 250, 'protein': 20, 'carbs': 25, 'fat': 5, 'mood_boost': 4},
            {'name': 'Whole Grain Toast with Avocado', 'category': 'breakfast', 'calories': 280, 'protein': 8, 'carbs': 35, 'fat': 12, 'mood_boost': 3},
            {'name': 'Smoothie Bowl', 'category': 'breakfast', 'calories': 320, 'protein': 12, 'carbs': 45, 'fat': 10, 'mood_boost': 4},

            # Lunch items
            {'name': 'Grilled Chicken Salad', 'category': 'lunch', 'calories': 350, 'protein': 35, 'carbs': 15, 'fat': 15, 'mood_boost': 4},
            {'name': 'Quinoa Bowl with Vegetables', 'category': 'lunch', 'calories': 400, 'protein': 15, 'carbs': 55, 'fat': 12, 'mood_boost': 3},
            {'name': 'Turkey Wrap with Veggies', 'category': 'lunch', 'calories': 380, 'protein': 28, 'carbs': 40, 'fat': 14, 'mood_boost': 3},
            {'name': 'Lentil Soup with Whole Grain Bread', 'category': 'lunch', 'calories': 420, 'protein': 18, 'carbs': 60, 'fat': 8, 'mood_boost': 4},

            # Dinner items
            {'name': 'Baked Salmon with Sweet Potato', 'category': 'dinner', 'calories': 450, 'protein': 35, 'carbs': 30, 'fat': 22, 'mood_boost': 5},
            {'name': 'Stir-fried Tofu with Brown Rice', 'category': 'dinner', 'calories': 380, 'protein': 20, 'carbs': 45, 'fat': 12, 'mood_boost': 3},
            {'name': 'Grilled Turkey with Quinoa', 'category': 'dinner', 'calories': 420, 'protein': 40, 'carbs': 35, 'fat': 14, 'mood_boost': 4},
            {'name': 'Vegetable Curry with Chickpeas', 'category': 'dinner', 'calories': 380, 'protein': 15, 'carbs': 50, 'fat': 10, 'mood_boost': 4},

            # Snacks (for mood boosting)
            {'name': 'Dark Chocolate (70%+)', 'category': 'snack', 'calories': 150, 'protein': 2, 'carbs': 12, 'fat': 10, 'mood_boost': 5},
            {'name': 'Mixed Nuts', 'category': 'snack', 'calories': 200, 'protein': 6, 'carbs': 8, 'fat': 18, 'mood_boost': 3},
            {'name': 'Apple with Peanut Butter', 'category': 'snack', 'calories': 180, 'protein': 5, 'carbs': 20, 'fat': 10, 'mood_boost': 4},
            {'name': 'Banana with Almonds', 'category': 'snack', 'calories': 220, 'protein': 4, 'carbs': 30, 'fat': 12, 'mood_boost': 4},
        ]

        # Create food items
        for food in food_data:
            FoodItem.objects.create(**food)
            self.stdout.write(f'Created: {food["name"]}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated {len(food_data)} food items')
        )
