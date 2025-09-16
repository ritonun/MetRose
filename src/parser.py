import pandas as pd


def load_data():
    ''' Load all gtfs .txt files into their respective pandas DataFrame '''

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
        try:
            data[key] = pd.read_csv(f"{path}/{key}.txt")
        except FileNotFoundError:
            print(f"File {path}/{key}.txt not found. Continuing without it.")
            data[key] = pd.DataFrame()
    return data


if __name__ == '__main__':
    data = load_data()
