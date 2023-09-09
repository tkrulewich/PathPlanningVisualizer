import os
import random
import base64
import json
import matplotlib.pyplot as plt
import matplotlib.animation
from flask import Flask, request, render_template
from PathPlanning import Grid, Obstacle
from time import time
from io import BytesIO

app = Flask(__name__)

@app.route("/find_path", methods=["POST"])
def find_path():
    """Finds a path between two points on a grid and returns the path as a base64 encoded video in a json response
    """
    content = request.get_json()

    algorithm = content["algorithm"]
    obstacles = content["obstacles"]
    start = content["start"]
    end = content["end"]

    grid_height = content["grid_height"]
    grid_width = content["grid_width"]

    grid_spacing = 0.5

    grid = Grid(0, grid_width, 0, grid_height, 0.5)

    for obstacle in obstacles:
        grid.add_obstacle(Obstacle(obstacle[0], obstacle[1], 1))
    
    fig = plt.figure(1)
    grid.inflate(0.5)

    start = grid.get_node(start[0], start[1])
    end = grid.get_node(end[0], end[1])

    # draw a blue triangle at the start and end

    plt.scatter(start.x, start.y, marker=(3, 0, 0), color="blue", s=50)
    plt.scatter(end.x, end.y, marker=(3, 0, 0), color="blue", s=50)

    t0 = time()

    x = []
    y = []

    if algorithm == "A*":
        x, y = grid.a_star(start, end)
    elif algorithm == "Dijkstra":
        x, y = grid.dijkstras(start, end)
    elif algorithm == "RRT":
        x, y, a = grid.RRT(start, end)

    t1 = time()

    grid.draw()

    x.reverse()
    y.reverse()


    path_line, = plt.plot(x, y, color='red')

    # set ax equal

    ax = plt.gca().set_aspect('equal', adjustable='box')

    # set the background to dark grey

    ax = fig.set_facecolor('#282c34')

    # make tick color white

    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')

    def update(frame):
        path_line.set_data(x[:frame], y[:frame])
        return path_line,

    anim = matplotlib.animation.FuncAnimation(fig, update, frames=range(0, len(x)+1, 4),blit=True, interval=50)

    # save the animation as an mp4 but speed up the fps

    # random filename


    filename = "static/" + str(random.randint(0, 1000000)) + ".mp4"

    while os.path.exists(filename):
        filename = "static/" + str(random.randint(0, 1000000)) + ".mp4"

    anim.save(filename, fps=12, extra_args=['-vcodec', 'libx264',])

    #load the video file into memory

    with open(filename, "rb") as f:
        video = f.read()
    
    # delete the video file

    os.remove(filename)

    # close the figure

    plt.close()

    # send a json response with the video file

    data = {"video": base64.b64encode(video).decode("utf-8")}
    data["path_length"] = end.cost
    data["path_time"] = t1 - t0

    return json.dumps(data)



@app.route("/make_grid", methods=["POST"]) 
def make_grid():
    """Creates a grid Image with obstacles and returns information about the grid with a plot as a base64 encoded image in a json response"""
    content = request.get_json()

    grid_height = content["grid_height"]
    grid_width = content["grid_width"]

    num_obstacles = content["num_obstacles"]

    grid_spacing = 0.5
    grid = Grid(0, grid_width, 0, grid_height, grid_spacing)

    for i in range(0, num_obstacles):
        x = random.randint(0, grid_width)
        y = random.randint(0, grid_height)

        grid.add_obstacle(Obstacle(x, y, 1))

    
    # get random start and end points

    grid.inflate(0.5)



    start = list(grid.valid_nodes)[random.randint(0, len(grid.valid_nodes) - 1)]
    end = list(grid.valid_nodes)[random.randint(0, len(grid.valid_nodes) - 1)]

    while start == end or start.distance(end) < max(grid_width, grid_height) / 2:
        start = list(grid.valid_nodes)[random.randint(0, len(grid.valid_nodes) - 1)]
        end = list(grid.valid_nodes)[random.randint(0, len(grid.valid_nodes) - 1)]
    
    # draw a blue triangle at the start and end

    plt.scatter(start.x, start.y, marker=(3, 0, 0), color="blue", s=50)
    plt.scatter(end.x, end.y, marker=(3, 0, 0), color="blue", s=50)


    fig = plt.figure(1)


    grid.draw()

    # set ax equal

    ax = plt.gca().set_aspect('equal', adjustable='box')

    # set the background to dark grey

    ax = fig.set_facecolor('#282c34')

    # make tick color white

    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')

    # save the figure as a png into buffer

    buf = BytesIO()

    plt.savefig(buf, format="png")

    # close the figure

    plt.close()

    # send a json response with the image file

    data = {"image": base64.b64encode(buf.getbuffer()).decode("utf-8")}
    data["obstacles"] = [[obstacle.x, obstacle.y] for obstacle in grid.obstacles]
    data["start"] = [start.x, start.y]
    data["end"] = [end.x, end.y]

    return json.dumps(data)



if __name__ == "__main__":
    app.run(debug=True)