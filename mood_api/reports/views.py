import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import ChatMessage
from .serializers import ChatMessageSerializer

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def chat(self, request):
        """Send message to AI assistant and get response"""
        message = request.data.get('message', '').strip()

        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Call Hugging Face Inference API
            response = self._call_hugging_face_api(message)

            # Save conversation to database
            chat_message = ChatMessage.objects.create(
                user=request.user,
                message=message,
                response=response
            )

            serializer = self.get_serializer(chat_message)
            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _call_hugging_face_api(self, message):
        """Call Hugging Face Inference API for nutrition/mood advice"""
        try:
            headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
            API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

            # Prompt tuned for conversational nutrition advice
            prompt = f"I'm a nutrition assistant. {message}"

            payload = {
                "inputs": {
                    "past_user_inputs": [],
                    "generated_responses": [],
                    "text": prompt
                },
                "parameters": {
                    "max_length": 200,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            }

            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()

                # BlenderBot returns a list with dicts containing 'generated_text'
                if isinstance(result, list) and "generated_text" in result[0]:
                    advice = result[0]["generated_text"].strip()
                    return advice if len(advice) > 5 else self._get_fallback_response(message)

                return self._get_fallback_response(message)

            else:
                # Expose error message for debugging
                raise Exception(f"Hugging Face API error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return self._get_fallback_response(message)
        except Exception as e:
            print(f"Unexpected Hugging Face API error: {e}")
            return self._get_fallback_response(message)

    def _get_fallback_response(self, message):
        """Provide intelligent fallback responses based on user message"""
        message_lower = message.lower()

        # Mood-related queries
        if any(word in message_lower for word in ["mood", "happy", "sad", "depress", "anxiety", "stress", "mental", "emotion"]):
            return "For mood improvement, try foods rich in omega-3 fatty acids like salmon, walnuts, and flaxseeds. Also, complex carbohydrates from whole grains can help stabilize blood sugar and mood. Regular exercise and adequate sleep are also crucial for mental well-being."

        # Hydration queries
        elif any(word in message_lower for word in ["water", "drink", "hydrate", "thirst"]):
            return "The general recommendation is about 8 glasses (2 liters) of water per day, but this varies by individual factors like activity level, climate, and health conditions. Listen to your body's thirst signals and aim for clear or light yellow urine as a good indicator of hydration."

        # Sleep queries
        elif any(word in message_lower for word in ["sleep", "insomnia", "rest", "bedtime"]):
            return "For better sleep, maintain a consistent sleep schedule, create a relaxing bedtime routine, and avoid screens 1-2 hours before bed. Foods that promote sleep include those containing tryptophan (turkey, bananas), magnesium (nuts, leafy greens), and melatonin (cherries, almonds)."

        # Energy queries
        elif any(word in message_lower for word in ["energy", "tired", "fatigue", "boost", "alert"]):
            return "To boost energy naturally, focus on balanced meals with complex carbohydrates, lean proteins, and healthy fats. Stay hydrated, get regular exercise, and consider iron-rich foods like spinach and lentils if you're feeling chronically fatigued. B vitamins from whole grains and lean meats also support energy production."

        # Breakfast queries
        elif any(word in message_lower for word in ["breakfast", "morning", "start day"]):
            return "A good breakfast should include protein, healthy fats, and complex carbohydrates. Try oatmeal with nuts and fruit, Greek yogurt with berries and granola, or eggs with whole grain toast and avocado. This combination provides sustained energy and helps maintain stable blood sugar throughout the morning."

        # Weight/fat related queries
        elif any(word in message_lower for word in ["weight", "fat", "lose", "gain", "diet", "calorie"]):
            return "For healthy weight management, focus on nutrient-dense whole foods, maintain a calorie balance appropriate for your goals, and include regular physical activity. Foods like vegetables, lean proteins, whole grains, and healthy fats support sustainable weight changes. Consider consulting a healthcare professional for personalized advice."

        # Meal planning queries
        elif any(word in message_lower for word in ["meal", "plan", "menu", "food map", "sunday", "monday", "diet plan"]):
            return "A balanced meal plan should include vegetables, lean proteins, whole grains, and healthy fats. For example, a typical day might include: Breakfast - oatmeal with fruit and nuts; Lunch - grilled chicken salad with quinoa; Dinner - baked salmon with vegetables and brown rice; Snacks - Greek yogurt or apple with almond butter. Adjust portions based on your individual needs."

        # General nutrition queries
        elif any(word in message_lower for word in ["food", "eat", "nutrition", "healthy", "diet"]):
            return "Focus on whole, unprocessed foods including plenty of vegetables, fruits, lean proteins, whole grains, and healthy fats. The Mediterranean diet is a great template: lots of plant foods, olive oil, fish, nuts, and limited red meat and sweets. Listen to your body's hunger and fullness cues."

        # Exercise queries
        elif any(word in message_lower for word in ["exercise", "workout", "fitness", "active"]):
            return "Regular physical activity is great for both physical and mental health. Aim for 150 minutes of moderate aerobic activity or 75 minutes of vigorous activity per week, plus strength training twice weekly. Find activities you enjoy and start small to build sustainable habits."

        else:
            return "I'm here to help with nutrition and mood advice! I can provide guidance on healthy eating, mood-boosting foods, sleep nutrition, hydration, exercise, weight management, and wellness tips. What specific topic would you like to know more about?"
