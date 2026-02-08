import pandas as pd
import random

def generate_satellite():
    return {
        "semi_major_axis": random.uniform(6700, 7200),  # km
        "eccentricity": random.uniform(0.0001, 0.01),
        "inclination": random.uniform(0, 98),          # degrees
        "raan": random.uniform(0, 360),                # degrees
        "arg_perigee": random.uniform(0, 360),         # degrees
        "mean_anomaly": random.uniform(0, 360),        # degrees
        "label": 0  # 0 = Active Satellite
    }

# Generate 500 sample satellites
satellites = [generate_satellite() for _ in range(500)]

# Convert to DataFrame
df = pd.DataFrame(satellites)

# Save to CSV
df.to_csv("satellite_data.csv", index=False)

print("Satellite dataset created with long column names!")
