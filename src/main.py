import pandas as pd

def load_data():
    path = "data/tisseo_gtfs_v2"
    keys = [
        "agency",
        "calendar",
        "calendar_dates",
        "routes",
        "shapes",
        "stop_times",
        "stops",
        "transfers",
        "trips"
    ]

    data = {}
    for key in keys:
        data[key] = pd.read_csv(f"{path}/{key}.txt")
    return data

if __name__ == '__main__':
    data = load_data()
    for key in data:
        print('\n')
        print(key)
        print(data[key].head())
