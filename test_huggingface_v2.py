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

def test_model(model_name):
    """Test if a specific model is available"""
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    url = f"https://api-inference.huggingface.co/models/{model_name}"

    # Simple test payload
    payload = {
        "inputs": "Hello, how are you?",
        "parameters": {"max_length": 50}
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"Model {model_name}: Status {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                print(f"✅ Model {model_name} works! Response: {result[0].get('generated_text', '')[:100]}...")
                return True
            else:
                print(f"❌ Model {model_name} returned empty result")
                return False
        elif response.status_code == 503:
            print(f"⚠️ Model {model_name} is loading (503). Try again later.")
            return False
        else:
            print(f"❌ Model {model_name} failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Model {model_name} error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Hugging Face API Key and Alternative Models...")
    print("=" * 60)

    # Test API key first
    if not test_api_key():
        print("Cannot proceed without valid API key")
        sys.exit(1)

    print("\nTesting alternative models that might be available...")
    print("=" * 60)

    # Test some models that are known to be available or might work
    alternative_models = [
        "microsoft/DialoGPT-small",
        "gpt2-medium",
        "distilbert-base-uncased",
        "bert-base-uncased",
        "roberta-base",
        "albert-base-v2",
        "t5-small",
        "google/t5-v1_1-small",
        "microsoft/phi-1_5",
        "bigscience/bloom-560m",
        "EleutherAI/gpt-neo-125m"
    ]

    working_models = []
    for model in alternative_models:
        if test_model(model):
            working_models.append(model)
        print("-" * 40)

    print(f"\nWorking models found: {len(working_models)}")
    for model in working_models:
        print(f"✅ {model}")

    if working_models:
        print(f"\nRecommended model: {working_models[0]}")
        print("You can update your reports/views.py to use this model.")
    else:
        print("\nNo working models found.")
        print("This could be due to:")
        print("1. Models not being available for inference")
        print("2. API rate limits or quota exceeded")
        print("3. Model loading issues on Hugging Face servers")
        print("4. Network connectivity issues")
        print("\nRecommendation: Continue using the intelligent fallback responses")
        print("which provide excellent nutrition and wellness advice without external dependencies.")
