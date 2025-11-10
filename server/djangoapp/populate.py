from .models import CarMake, CarModel

def initiate():
    # Clear existing data to avoid duplicates (optional, for testing)
    CarModel.objects.all().delete()
    CarMake.objects.all().delete()

    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    car_make_instances = []
    for data in car_make_data:
        make = CarMake.objects.create(name=data['name'], description=data['description'])
        car_make_instances.append(make)

    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": 1, "color": "Black"},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": 1, "color": "White"},
        {"name": "XTRAIL", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": 1, "color": "Silver"},
        {"name": "A-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1], "dealer_id": 2, "color": "Red"},
        {"name": "C-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1], "dealer_id": 2, "color": "Blue"},
        {"name": "E-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1], "dealer_id": 2, "color": "Black"},
        {"name": "A4", "type": "SUV", "year": 2023, "car_make": car_make_instances[2], "dealer_id": 3, "color": "White"},
        {"name": "A5", "type": "SUV", "year": 2023, "car_make": car_make_instances[2], "dealer_id": 3, "color": "Silver"},
        {"name": "A6", "type": "SUV", "year": 2023, "car_make": car_make_instances[2], "dealer_id": 3, "color": "Red"},
        {"name": "Sorrento", "type": "SUV", "year": 2023, "car_make": car_make_instances[3], "dealer_id": 4, "color": "Blue"},
        {"name": "Carnival", "type": "SUV", "year": 2023, "car_make": car_make_instances[3], "dealer_id": 4, "color": "Black"},
        {"name": "Cerato", "type": "Sedan", "year": 2023, "car_make": car_make_instances[3], "dealer_id": 4, "color": "White"},
        {"name": "Corolla", "type": "Sedan", "year": 2023, "car_make": car_make_instances[4], "dealer_id": 5, "color": "Silver"},
        {"name": "Camry", "type": "Sedan", "year": 2023, "car_make": car_make_instances[4], "dealer_id": 5, "color": "Red"},
        {"name": "Kluger", "type": "SUV", "year": 2023, "car_make": car_make_instances[4], "dealer_id": 5, "color": "Blue"},
    ]

    for data in car_model_data:
        obj = CarModel(
            name=data['name'],
            car_make=data['car_make'],
            type=data['type'],
            year=data['year'],
            dealer_id=data['dealer_id'],
            color=data['color']
        )
        obj.save()
        print(f"Saved CarModel: {obj.name} for {obj.car_make.name}")

    print(f"Total CarMakes: {CarMake.objects.count()}")
    print(f"Total CarModels: {CarModel.objects.count()}")