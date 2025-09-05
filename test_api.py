import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_login():
    """Test user login"""
    print("Testing login...")
    response = requests.post(f"{BASE_URL}/login/", json={
        "username": "testuser",
        "password": "testpass123"
    })
    print(f"Login status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Full response data: {data}")
        token = data.get('tokens', {}).get('access')
        print("Login successful!")
        if token:
            print(f"Token received: {token[:50]}...")
        else:
            print("No access token in response")
        return token
    else:
        print(f"Login failed: {response.text}")
        return None

def test_chat(token, message):
    """Test chat endpoint"""
    print(f"\nTesting chat with message: {message}")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(f"{BASE_URL}/chat/chat/", json={"message": message}, headers=headers)
    print(f"Chat status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"AI Response: {data.get('response', 'No response')}")
        return True
    else:
        print(f"Chat failed: {response.text}")
        return False

def test_logs(token):
    """Test logs endpoint"""
    print("\nTesting logs GET...")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{BASE_URL}/logs/", headers=headers)
    print(f"Logs GET status: {response.status_code}")

    print("Testing logs POST...")
    log_data = {
        "date": "2025-09-02",
        "mood": 4,
        "sleep_hours": 7.5,
        "exercise_minutes": 30,
        "food": "Breakfast: Oatmeal, Lunch: Chicken salad"
    }
    response = requests.post(f"{BASE_URL}/logs/", json=log_data, headers=headers)
    print(f"Logs POST status: {response.status_code}")
    if response.status_code != 201:
        print(f"Logs POST failed: {response.text}")

def test_food_suggestions(token):
    """Test food suggestions endpoint"""
    print("\nTesting food suggestions...")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{BASE_URL}/food-suggestions/", headers=headers)
    print(f"Food suggestions status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data)} food suggestions")

if __name__ == "__main__":
    # Test login
    token = test_login()
    if not token:
        print("Cannot proceed without login token")
        exit(1)

    # Test chat
    test_chat(token, "What foods can help improve my mood?")

    # Test logs
    test_logs(token)

    # Test food suggestions
    test_food_suggestions(token)

    print("\nAPI testing completed!")
