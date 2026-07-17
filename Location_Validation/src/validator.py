import json
import math
from .config import DATA_FILE, MAX_DISTANCE


class LocationValidator:

    def __init__(self):

        with open(DATA_FILE, "r") as f:
            self.points = json.load(f)

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):

        R = 6371000

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)

        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = (
            math.sin(dphi / 2) ** 2
            + math.cos(phi1)
            * math.cos(phi2)
            * math.sin(dlambda / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def validate(self, latitude, longitude):

        point = self.points[0]

        distance = self.haversine(
            latitude,
            longitude,
            point["latitude"],
            point["longitude"],
        )

        status = distance <= MAX_DISTANCE

        return (
            status,
            point["name"],
            round(distance, 2)
        )