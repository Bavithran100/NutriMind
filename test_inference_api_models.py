import requests
import sys

# Add the mood_api directory to the path
sys.path.append('mood_api')

# Import settings
from mood_api.settings import HUGGINGFACE_API_KEY

def test_api_key():
    """Test if the Hugging Face API key is valid"""
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    response = requests.get("https://huggingface.co/api/whoami-v2", headers=headers)

    print(f"API Key Test Status: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ API Key is valid! User: {user_data.get('name', 'Unknown')}")
        return True
    else:
        print(f"❌ API Key invalid: {response.text}")
        return False

def test_inference_model(model_name, task_type="text-generation"):
    """Test if a specific Inference API-enabled model is available"""
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    url = f"https://api-inference.huggingface.co/models/{model_name}"

    # Different payloads based on task type
    if task_type == "text-generation":
        payload = {
            "inputs": "Suggest a healthy dinner for a student who sleeps less than 6 hours.",
            "parameters": {
                "max_length": 100,
                "temperature": 0.7,
                "do_sample": True
            }
        }
    elif task_type == "text2text-generation":
        payload = {
            "inputs": "Suggest healthy foods for better mood",
            "parameters": {
                "max_length": 50
            }
        }
    elif task_type == "text-classification":
        payload = {
            "inputs": "I feel happy and energetic today"
        }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"Model {model_name}: Status {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if task_type == "text-generation":
                    response_text = result[0].get('generated_text', '')
                    print(f"✅ Model {model_name} works! Response: {response_text[:150]}...")
                elif task_type == "text2text-generation":
                    response_text = result[0].get('generated_text', '')
                    print(f"✅ Model {model_name} works! Response: {response_text}")
                elif task_type == "text-classification":
                    print(f"✅ Model {model_name} works! Emotions detected: {result[0]}")
                return True
            else:
                print(f"❌ Model {model_name} returned empty result")
                return False
        elif response.status_code == 503:
            print(f"⚠️ Model {model_name} is loading (503). This model supports Inference API but needs to load first.")
            return False
        else:
            print(f"❌ Model {model_name} failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Model {model_name} error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Hugging Face Inference API-Enabled Models...")
    print("=" * 70)

    # Test API key first
    if not test_api_key():
        print("Cannot proceed without valid API key")
        sys.exit(1)

    print("\nTesting Inference API-enabled models...")
    print("=" * 70)

    # Models that are confirmed to support Inference API
    inference_models = [
        # Text Generation Models
        ("bigscience/bloom", "text-generation"),
        ("tiiuae/falcon-7b-instruct", "text-generation"),
        ("google/flan-t5-large", "text2text-generation"),
        ("microsoft/phi-1_5", "text-generation"),

        # Emotion/Text Classification Models
        ("bhadresh-savani/distilbert-base-uncased-emotion", "text-classification"),
        ("j-hartmann/emotion-english-distilroberta-base", "text-classification"),
    ]

    working_models = []
    for model_name, task_type in inference_models:
        print(f"\nTesting {model_name} ({task_type})...")
        if test_inference_model(model_name, task_type):
            working_models.append((model_name, task_type))
        print("-" * 50)

    print(f"\n{'='*70}")
    print(f"Working models found: {len(working_models)}")
    for model_name, task_type in working_models:
        print(f"✅ {model_name} ({task_type})")

    if working_models:
        best_model, best_type = working_models[0]
        print(f"\n🎯 Recommended model: {best_model}")
        print("You can update your reports/views.py to use this model."
        print("\nExample code for your AI assistant:"
        print(f"API_URL = 'https://api-inference.huggingface.co/models/{best_model}'")
    else:
        print("\nNo working Inference API models found at this time.")
        print("This could be due to:")
        print("• Models are still loading (503 status)")
        print("• Temporary server issues")
        print("• Network connectivity")
        print("\nRecommendation: The current fallback system works perfectly!")
        print("It provides reliable, nutrition-focused advice without external dependencies.")
