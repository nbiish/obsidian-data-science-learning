import csv
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Michigan cities in Upper and Lower Peninsula
michigan_cities = {
    'Upper Peninsula': ['Marquette', 'Escanaba', 'Sault Ste. Marie', 'Houghton', 'Iron Mountain'],
    'Lower Peninsula': ['Detroit', 'Grand Rapids', 'Lansing', 'Ann Arbor', 'Kalamazoo', 'Flint', 'Traverse City', 'Petoskey']
}

# Generate data
data = []
for _ in range(5000):
    peninsula = random.choice(['Upper Peninsula', 'Lower Peninsula'])
    city = random.choice(michigan_cities[peninsula])

    row = [
        fake.first_name(),
        fake.last_name(),
        f"{fake.building_number()} {fake.street_name()}, {city}, MI {fake.zipcode_in_state('MI')}",
        random.choice('ABCDEFGHIJKLM')
    ]
    data.append(row)

# Write to CSV
with open('michigan_synthetic_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['First Name', 'Last Name', 'Address', 'Tribal Alpha Code'])
    writer.writerows(data)

print("\n\nCSV file 'michigan_synthetic_data.csv' has been created with 5000 rows of synthetic data.")