# map_visu.py
# visualise on flask the map
import folium


def create_map(line_coords, stations, train_positions=None, zoom_start=13):
    """Create a folium map for visualisation"""
    m = folium.Map(location=line_coords[0], zoom_start=zoom_start)

    # Add metro line
    folium.PolyLine(line_coords, color='blue', weight=5, opacity=0.7).add_to(m)

    # Add stations
    for s in stations:
        folium.CircleMarker(location=s, radius=5, color='red', fill=True).add_to(m)

    # Add simulated trains
    if train_positions:
        for t in train_positions:
            folium.CircleMarker(location=t, radius=7, color='green', fill=True).add_to(m)

    return m
