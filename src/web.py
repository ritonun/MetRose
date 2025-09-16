from flask import Flask, render_template
from parser import load_data, get_route_map_data
from map_visu import create_map

# create flask app
app = Flask(__name__)

# CONFIG
ROUTE_ID = "line:61"
SHAPE_ID = 11971

# load data
data = load_data()
stations_ma, line_coords_ma = get_route_map_data(data, "line:61", 11971)    # metro a
stations_mb, line_coords_mb = get_route_map_data(data, "line:69", 11973)    # metro b
line_coords = [line_coords_ma, line_coords_mb]
stations = [stations_ma, stations_mb]

@app.route('/')
def index():
    # Example train positions
    train_positions = [line_coords[0][0], line_coords[0][5]]

    # Create map
    m = create_map(line_coords, stations, train_positions=train_positions)
    map_html = m._repr_html_()
    return render_template("index.html", map_html=map_html)



if __name__ == "__main__":
    app.run(debug=True)
