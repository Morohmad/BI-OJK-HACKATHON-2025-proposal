from gps import GPS
from validator import LocationValidator
from logger import LocationLogger


gps = GPS()
validator = LocationValidator()
logger = LocationLogger()

location = gps.get_location()

valid, point_name, distance = validator.validate(
    location["latitude"],
    location["longitude"]
)

if valid:

    status = "VALID"

else:

    status = "INVALID"

print("=" * 40)
print("LOCATION VALIDATION")
print("=" * 40)

print("Distribution Point :", point_name)
print("Distance           :", distance, "meter")
print("Status             :", status)

logger.save(point_name, status, distance)