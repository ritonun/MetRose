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
stations, line_coords = get_route_map_data(data, ROUTE_ID, SHAPE_ID)

@app.route('/')
def index():
    # Example train positions
    train_positions = [line_coords[0], line_coords[5]]

    # Create map
    m = create_map(line_coords, stations, train_positions=train_positions)
    map_html = m._repr_html_()
    return render_template("index.html", map_html=map_html)



if __name__ == "__main__":
    app.run(debug=True)
