import pandas as pd
import matplotlib.pyplot as plt


def plot_route(route_id, data):
    # Select trips for this route
    trips_for_route = data["trips"][data["trips"]["route_id"] == str(route_id)]
    if trips_for_route.empty:
        print(f"No trips found for route {route_id}")
        return

    # Use the first trip as an example
    trip_id = trips_for_route.iloc[0]["trip_id"]
    trip_stop_times = (
        data["stop_times"][data["stop_times"]["trip_id"] == trip_id]
        .sort_values("stop_sequence")
    )
    trip_stops = trip_stop_times.merge(data["stops"], on="stop_id")

    plt.figure(figsize=(10, 7))

    # Plot shape if available
    if "shapes" in data and "shape_id" in trips_for_route.columns:
        shape_id = trips_for_route.iloc[0]["shape_id"]
        shape_points = (
            data["shapes"][data["shapes"]["shape_id"] == shape_id]
            .sort_values("shape_pt_sequence")
        )
        if not shape_points.empty:
            plt.plot(
                shape_points["shape_pt_lon"],
                shape_points["shape_pt_lat"],
                color="blue",
                linewidth=2,
                label="Route Shape"
            )

    # Plot stops
    plt.scatter(
        trip_stops["stop_lon"],
        trip_stops["stop_lat"],
        c="red",
        s=40,
        zorder=5,
        label="Stops"
    )

    # Annotate stops
    for _, row in trip_stops.iterrows():
        plt.text(row["stop_lon"], row["stop_lat"], row["stop_name"], fontsize=8)

    # Title with route info
    route_info = data["routes"][data["routes"]["route_id"] == str(route_id)]
    if not route_info.empty:
        route_name = route_info.iloc[0].get("route_short_name", route_id)
        title = f"Route {route_name} ({route_id})"
    else:
        title = f"Route {route_id}"

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(title)
    plt.legend()
    plt.savefig("doc/t1.png")

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
    print("data loaded")

    route_id = "line:68"   # tram T1
    plot_route(route_id, data)
