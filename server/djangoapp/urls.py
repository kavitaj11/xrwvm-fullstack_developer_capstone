from django.urls import path
from . import views

urlpatterns = [
    # ✅ Home page mapped to root
    path("", views.index, name="home"),
    path("dealers/", views.dealers, name="dealers"),
    # Authentication
    path("register/", views.registration, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_request, name="logout"),

    # Dealership APIs
    path("dealers/", views.get_dealerships, name="dealers"),
    path(
        "dealers/<str:state>/",
        views.get_dealerships,
        name="dealers_by_state",
    ),

    # Dealer details + reviews
    path(
        "dealer/<int:dealer_id>/",
        views.get_dealer_details,
        name="dealer_details",
    ),
    path(
        "reviews/dealer/<int:dealer_id>/",
        views.get_dealer_reviews,
        name="dealer_reviews",
    ),
    path("add_review/", views.add_review, name="add_review"),
    path(
        route="get_dealers/",
        view=views.get_dealerships,
        name="get_dealers"
    ),
    # Cars API
    path("get_cars/", views.get_cars, name="getcars"),
]
