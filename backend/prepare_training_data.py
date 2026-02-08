import pandas as pd

# Load original debris
debris = pd.read_csv("debris_dataset.csv")

# Load generated satellites
sat = pd.read_csv("satellite_data.csv")

# Combine
final = pd.concat([debris, sat], ignore_index=True)

# Save back as debris_dataset.csv (overwrite)
final.to_csv("debris_dataset.csv", index=False)

print("Debris + Satellite merged into debris_dataset.csv")
