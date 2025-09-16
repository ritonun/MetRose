# map_visu.py
# visualise on flask the map
import folium


def create_map(lines_coords, all_stations, train_positions=None, zoom_start=13):
    """Create a folium map for visualisation"""
    m = folium.Map(location=lines_coords[0][0], zoom_start=zoom_start)

    # Add metro line
    color = ["red", "yellow"]
    i = 0
    for line_coords in lines_coords:
        folium.PolyLine(line_coords, color=color[i], weight=5, opacity=0.7).add_to(m)
        i += 1

    # Add stations
    color = ["white", "purple"]
    i = 0
    for stations in all_stations:
        for s in stations:
            folium.CircleMarker(location=s, radius=5, color=color[i], fill=True).add_to(m)
        i += 1

    # Add simulated trains
    if train_positions:
        for t in train_positions:
            folium.CircleMarker(location=t, radius=7, color='green', fill=True).add_to(m)

    return m
