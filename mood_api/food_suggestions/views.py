from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FoodItem
from .serializers import FoodItemSerializer

class FoodSuggestionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # For simplicity, return all food items as suggestions
        foods = FoodItem.objects.all()
        serializer = FoodItemSerializer(foods, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def suggest(self, request):
        # Placeholder for advanced AI-based suggestions using Hugging Face API
        # For now, return a static meal plan
        meal_plan = {
            "breakfast": "Oats + Banana",
            "lunch": "Rice + Chicken + Salad",
            "dinner": "Soup + Spinach"
        }
        return Response(meal_plan)
