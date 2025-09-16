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


def get_trips_from_route(data, route_id):
    return data["trips"][data["trips"]["route_id"] == route_id]["trip_id"].unique()

def get_stop_ids_for_trips(data, trip_ids):
    return data["stop_times"][data["stop_times"]['trip_id'].isin(trip_ids)]['stop_id'].unique()

def get_station_coords(data, stop_ids):
    """Return (lattitude, longitude) of given stop ids (list)"""
    clean_stop_ids = [s.replace('stop_area:', '') for s in stop_ids]
    return data["stops"][data["stops"]['stop_id'].str.replace('stop_area:', '', regex=False)
                    .isin(clean_stop_ids)][['stop_lat', 'stop_lon']].values.tolist()

def get_line_coords(data, shape_id):
    """Return (lattitude, longitude) coord for a given shape id"""
    return data["shapes"][data["shapes"]['shape_id'] == shape_id][['shape_pt_lat', 'shape_pt_lon']].values.tolist()

def get_route_map_data(data, ROUTE_ID, SHAPE_ID):
    trips_ids = get_trips_from_route(data, ROUTE_ID)
    stops_ids = get_stop_ids_for_trips(data, trips_ids)
    stations = get_station_coords(data, stops_ids)
    line_coords = get_line_coords(data, SHAPE_ID)
    return stations, line_coords


if __name__ == '__main__':
    data = load_data()
