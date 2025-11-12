import os
import requests
from dotenv import load_dotenv
import requests
import json
import logging

# 👇 Add this constant here
sentiment_url = "https://sentiment.22l0kxzcvcxt.us-south.codeengine.appdomain.cloud"

logger = logging.getLogger(__name__)

load_dotenv()

# Backend services
backend_url = os.getenv(
    'backend_url', 
    default="http://localhost:3030"
)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
     default="http://localhost:5050/"
)


# ----------------------- GET REQUEST (Dealers / Reviews) ----------------------- #
def get_request(endpoint, **params):
    """
    Calls backend microservice on localhost:3030
    Ex: get_request("/fetchReviews/dealer/10")
    """
    url = f"{backend_url.rstrip('/')}/{endpoint.lstrip('/')}"
    print("➡️ GET:", url, params)

    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print("❌ Network error:", e)
        return {"status": "error", "message": str(e)}


# ----------------------- POST REVIEW (CRUD microservice) ----------------------- #
def post_review(review_payload, dealer_id):
    """
    Send review to backend database microservice
    """
    url = f"{backend_url.rstrip('/')}/postreview/{dealer_id}"
    print("➡️ POST:", url, review_payload)

    try:
        response = requests.post(url, json=review_payload)
        return response.json()
    except Exception as e:
        print("❌ Error posting review:", e)
        return {"status": "error", "message": str(e)}


# ----------------------- SENTIMENT ANALYZER (Flask microservice @5000) ----------------------- #
def analyze_review_sentiments(text):
    """
    Calls sentiment analyzer microservice.
    GET http://127.0.0.1:5000/analyze/<text>
    """
    url = f"{sentiment_url.rstrip('/')}/analyze/{text}"
    print("➡️ Sentiment Request:", url)

    try:
        response = requests.get(url)
        json_response = response.json()
        # Expect label: positive/neutral/negative
        return json_response.get("label", "neutral")

    except Exception as e:
        print("❌ Sentiment API error:", e)
        return "neutral"
