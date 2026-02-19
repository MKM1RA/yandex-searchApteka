import os
import sys
import requests
import arcade
from distance import lonlat_distance
from utils import get_spn

GEO_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
SEARCH_KEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
STATIC_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"


class PharmacyMap(arcade.Window):
    def __init__(self, address):
        super().__init__(600, 450, "Поиск аптеки 2.0")
        self.address = address
        self.background = None

    def setup(self):
        geo_params = {"apikey": GEO_KEY, "geocode": self.address, "format": "json"}
        geo_res = requests.get("http://geocode-maps.yandex.ru/1.x/", params=geo_params).json()
        toponym = geo_res["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        user_lonlat = tuple(map(float, toponym["Point"]["pos"].split()))

        search_params = {
            "apikey": SEARCH_KEY, "text": "аптека", "lang": "ru_RU",
            "ll": f"{user_lonlat[0]},{user_lonlat[1]}", "type": "biz"
        }
        search_res = requests.get("https://search-maps.yandex.ru/v1/", params=search_params).json()
        pharmacy = search_res["features"][0]

        ph_props = pharmacy["properties"]["CompanyMetaData"]
        ph_coords = pharmacy["geometry"]["coordinates"]
        dist = lonlat_distance(user_lonlat, ph_coords)

        print(f"Адрес: {ph_props['address']}\nНазвание: {ph_props['name']}")
        print(f"Время работы: {ph_props.get('Hours', {}).get('text', 'не указано')}")
        print(f"Расстояние: {round(dist)} м.")

        spn = get_spn(pharmacy)

        map_params = {
            "apikey": STATIC_KEY,
            "l": "map",
            "pt": f"{user_lonlat[0]},{user_lonlat[1]},pm2rdl~{ph_coords[0]},{ph_coords[1]},pm2dgl",
            "spn": spn
        }

        map_res = requests.get("https://static-maps.yandex.ru/v1", params=map_params)
        with open("map.png", "wb") as f:
            f.write(map_res.content)
        self.background = arcade.load_texture("map.png")

    def on_draw(self):
        self.clear()
        if self.background:
            arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0, self.width, self.height))


if __name__ == "__main__":
    addr = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Введите адрес: ")
    window = PharmacyMap(addr)
    window.setup()
    arcade.run()
    if os.path.exists("map.png"):
        os.remove("map.png")