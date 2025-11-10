# Uncomment the required imports before adding the code

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
import requests
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments

# Get an instance of a logger
logger = logging.getLogger(__name__)

# URL of your sentiment / dealership microservice running in IBM Code Engine
# Flask CRUD backend (dealers + reviews)
backend_url = "http://127.0.0.1:3030"
sentiment_url = "http://127.0.0.1:5000"  # Sentiment microservice


# Create your views here.


# ✅ Render Home / Index
def index(request):
    return render(request, "djangoapp/home.html")


# Static Page: ABOUT


def about(request):
    return render(request, "djangoapp/about.html")


# Static Page: CONTACT


def contact(request):
    return render(request, "djangoapp/contact.html")


def dealers(request):
    # Get selected state from GET query param (default: All)
    state = request.GET.get("state", "All")

    # Build the API endpoint
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"

    # Fetch data from backend microservice
    dealerships = get_request(endpoint)

    # Extract unique states from returned data
    states = sorted(list(set([dealer["state"] for dealer in dealerships])))

    return render(
        request,
        "djangoapp/dealers.html",
        {
            "dealerships": dealerships,
            "states": states,
            "selected_state": state,
        },
    )


# ✅ Registration View
def registration(request):
    if request.method == "GET":
        return render(request, "djangoapp/register.html")

    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return render(request, "djangoapp/register.html")

        # Create new user
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        login(request, user)
        return redirect("home")  # redirect to home page after registration


# ✅ Login View
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # ✅ Auto redirect to home
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")  # Reload login page

    return render(request, "djangoapp/login.html")


def logout_request(request):
    logout(request)
    return redirect("home")


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name,
                    "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})


# Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        # <-- capitalize fixes kansas → Kansas
        endpoint = f"/fetchDealers/{state.capitalize()}"

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)

        # Add sentiment to each review
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail["review"])
            review_detail["sentiment"] = response["sentiment"]

        return render(
            request,
            "djangoapp/dealer_details.html",
            {
                "dealer_id": dealer_id,
                "reviews": reviews,
            },
        )

    return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if not dealer_id:
        messages.error(request, "Dealer ID missing.")
        return redirect("dealers")

    # Fetch dealership info
    dealership = get_request(f"/fetchDealer/{dealer_id}")

    if not dealership:
        messages.error(request, "Dealer not found.")
        return redirect("dealers")

    # ✅ Fetch reviews (IBM backend returns key `reviews` not raw list sometimes)
    response = get_request(f"/fetchReviews/dealer/{dealer_id}") or {}

    # If backend returns {"reviews": [...]}, use that list
    reviews = (
        response.get("reviews", response) if isinstance(
            response, dict) else response
    )

    sanitized_reviews = []
    for review in reviews:
        if not isinstance(review, dict):
            continue  # skip None or malformed entries

        review_text = review.get("review", "")
        sentiment = analyze_review_sentiments(review_text)
        review["sentiment"] = sentiment or "neutral"

        sanitized_reviews.append(review)

    return render(
        request,
        "djangoapp/dealer_details.html",
        {
            "dealer": dealership,
            "reviews": sanitized_reviews,
        },
    )


def post_review_to_backend(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return {"error": "Could not post review"}


# Create a `add_review` view to submit a review


@login_required
def add_review(request):
    if request.method == "GET":
        dealer_id = request.GET.get("dealer_id")

        if not dealer_id:
            messages.error(request, "Dealer ID missing.")
            return redirect("dealers")

        # Ensure database has car makes/models (only runs once)
        if not CarMake.objects.exists():
            initiate()

        cars = CarModel.objects.select_related("car_make").order_by(
            "car_make__name", "name"
        )

        # get dealer details for display on page
        dealer = get_request(f"/fetchDealer/{dealer_id}")

        return render(
            request,
            "djangoapp/add_review.html",
            {
                "dealer_id": dealer_id,
                "cars": cars,
                "dealer": dealer,
            },
        )

    # ---------- POST ----------
    elif request.method == "POST":
        dealer_id = request.POST.get("dealer_id")
        car_id = request.POST.get("car_id")

        if not dealer_id or not car_id:
            messages.error(
                request, "Please select a dealer and a car before submitting."
            )
            return redirect("dealers")

        # Find selected car
        car = CarModel.objects.select_related("car_make").get(id=car_id)

        # Prepare payload matching backend microservice requirements
        payload = {
            "name": request.user.username,
            "dealership": int(dealer_id),
            "review": request.POST.get("review", "").strip(),
            "purchase": request.POST.get("purchasecheck") == "on",
            "purchase_date": request.POST.get("purchase_date")
            or datetime.now().strftime("%m/%d/%Y"),
            "car_make": car.car_make.name,
            "car_model": car.name,
            "car_year": str(car.year),  # ✅ FIXED HERE
        }

        # Call microservice to insert review
        post_review_to_backend(payload)

        messages.success(request, "Review submitted successfully!")
        return redirect("dealer_details", dealer_id=dealer_id)
