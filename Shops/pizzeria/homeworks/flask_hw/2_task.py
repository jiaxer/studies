"""
Запустите приложение, посмотрите, как оно сейчас работает
Сделайте так, чтобы при переходе по
localhost:5000/cars

Выводился json следующего формата:
{
    "cars_number": 25,
    "cars": [
        {
            "id": 101068323,
            "price_usd": 22300,
            "brand": "Nissan",
            "model": "Leaf",
            "generation": "II",
            "year": "2017",
            "rain_detector": true,
            "interior_material": "ткань",
            "created_advert": "2022-05-01T18:59:04+0000"
        },
        ...
    ]
}

(extra) Дабавьте фильтрацию через адресную строку по всем этим параметрам.
"""

import json
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


class CarsStorage:

    def __init__(self, path):
        self.path = path
        self.data = self.read()

    def find_cars(self, **kwargs) -> list:
        filters = {
            "id": lambda car: car.get("id") == kwargs.get('car_id'),
            "price_usd": lambda car: car.get("price_usd") == kwargs.get("price_usd"),
            "brand": lambda car: car.get("brand") == kwargs.get("brand").capitalize(),
            "model": lambda car: car.get("model") == kwargs.get("model").capitalize(),
            "year": lambda car: car.get("year") == kwargs.get("year"),
            "rain_detector": lambda car: car.get("rain_detector") == kwargs.get("rain_detector"),
            "generation": lambda car: car.get("generation") == kwargs.get("generation"),
            "interior_material": lambda car: car.get("interior_material") == kwargs.get("interior_material"),
            "created_advert": lambda car: car.get("created_advert") == kwargs.get("created_advert")
        }

        response = self.get_all_cars().get("cars")

        for key in kwargs.keys():
            response = filter(filters.get(key), response)

        return list(response)

    def get_car_by_id(self, car_id):
        return self.find_cars(car_id=str(car_id))

    def get_all_cars(self):
        result = {"cars_number": len(self.data)}
        cars = []
        for car in self.data:
            car_data = {
                "id": car.get("id"),
                f"price_{car.get('price').get('currency')}": car.get("price").get("amount"),
                "created_advert": car.get("publishedAt")
            }

            car_data.update(
                {car_property.get('name'): car_property.get("value") for car_property in car.get('properties')}
            )
            cars.append(car_data)
        result.update({"cars": cars})

        return result

    def save(self):
        with open(self.path, "w") as file:
            json.dump(file, self.data)

    def read(self):
        with open(self.path) as file:
            data = json.load(file).get("2_task").get("cars")
        return data


@app.route("/cars/", methods=["GET"])
def get_cars_view():
    get_args = request.args.to_dict()
    cars = CarsStorage("storage.json")
    if get_args:
        result = cars.find_cars(**get_args)
    else:
        result = cars.get_all_cars()
    return jsonify(result)


app.run(port=5000)
