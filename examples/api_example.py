"""
API Server Examples for SensitiveWordDetector
FastAPI-based REST API usage examples
"""

# Example 1: Start the API server
# Run: uvicorn sensitive_word_api:app --reload --host 0.0.0.0 --port 8000

import requests
import json


def api_examples():
    """Examples of using the API endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("API Examples")
    print("=" * 60)
    
    # 1. Health Check
    print("\n1. Health Check")
    response = requests.get(f"{base_url}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 2. Get Statistics
    print("\n2. Get Word List Statistics")
    response = requests.get(f"{base_url}/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 3. Detect Sensitive Words
    print("\n3. Detect Sensitive Words")
    payload = {
        "text": "这是一个包含敏感词的测试文本",
        "case_sensitive": False
    }
    response = requests.post(
        f"{base_url}/detect",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 4. Replace Sensitive Words
    print("\n4. Replace Sensitive Words")
    payload = {
        "text": "这是一个包含敏感词的测试文本",
        "replace_char": "*",
        "show_count": True
    }
    response = requests.post(
        f"{base_url}/replace",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 5. Batch Detect
    print("\n5. Batch Detect")
    payload = [
        "这是正常文本",
        "包含敏感词的内容",
        "正常文本",
    ]
    response = requests.post(
        f"{base_url}/batch_detect",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 6. Get All Words
    print("\n6. Get All Sensitive Words")
    response = requests.get(f"{base_url}/words")
    print(f"Status: {response.status_code}")
    words = response.json()["words"]
    print(f"Total words: {len(words)}")
    print(f"First 10 words: {words[:10]}")
    
    # 7. Reload Word List
    print("\n7. Reload Word List")
    response = requests.post(f"{base_url}/reload")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def api_usage_patterns():
    """Common API usage patterns"""
    
    print("\n" + "=" * 60)
    print("API Usage Patterns")
    print("=" * 60)
    
    # Pattern 1: Content Moderation
    print("\nPattern 1: Content Moderation")
    print("""
    def moderate_content(text):
        response = requests.post(
            "http://localhost:8000/detect",
            json={"text": text}
        )
        result = response.json()
        return not result["has_sensitive"]
    """)
    
    # Pattern 2: Auto-correction
    print("\nPattern 2: Auto-correction")
    print("""
    def auto_correct(text):
        response = requests.post(
            "http://localhost:8000/replace",
            json={
                "text": text,
                "replace_char": "*",
                "show_count": True
            }
        )
        return response.json()["result"]
    """)
    
    # Pattern 3: Batch Processing
    print("\nPattern 3: Batch Processing")
    print("""
    def process_batch(texts):
        response = requests.post(
            "http://localhost:8000/batch_detect",
            json=texts
        )
        return response.json()["results"]
    """)


if __name__ == '__main__':
    api_examples()
    api_usage_patterns()
