import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_ROOT = os.path.join(BASE_DIR, "..", "data")

def read_folder(folder_path, label):
    rows = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".dat"):
                path = os.path.join(root, file)

                with open(path, "r") as f:
                    for line in f:
                        parts = line.strip().split()

                        if len(parts) == 7:
                            values = list(map(float, parts[1:7]))
                            values.append(label)
                            rows.append(values)

    return rows


def load_full_dataset():
    debris_path = os.path.join(DATA_ROOT, "deb_train")
    sat_path = os.path.join(DATA_ROOT, "sat")

    debris_rows = read_folder(debris_path, label=1)
    sat_rows = read_folder(sat_path, label=0)

    print("Debris samples:", len(debris_rows))
    print("Satellite samples:", len(sat_rows))

    all_rows = debris_rows + sat_rows

    df = pd.DataFrame(all_rows, columns=[
        "semi_major_axis",
        "eccentricity",
        "inclination",
        "raan",
        "arg_perigee",
        "mean_anomaly",
        "label"
    ])

    return df


if __name__ == "__main__":
    df = load_full_dataset()
    csv_path = os.path.join(BASE_DIR, "debris_dataset.csv")
    df.to_csv(csv_path, index=False)
    print("✅ Combined dataset created!")
