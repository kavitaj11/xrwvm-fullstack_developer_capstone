# Uncomment the following imports before adding the Model code

# from django.db import models
# from django.utils.timezone import now
# from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=50, blank=True, null=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.country})" if self.country else self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(
        CarMake, on_delete=models.CASCADE, related_name="models"
    )  # Many-to-One relationship
    dealer_id = models.IntegerField()  # Refers to dealer in Cloudant DB
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        # Add more choices as required
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default="SUV")
    year = models.IntegerField(
        default=2023, validators=[MaxValueValidator(2023), MinValueValidator(2015)]
    )
    color = models.CharField(
        max_length=30, blank=True, null=True
    )  # Optional extra field

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
