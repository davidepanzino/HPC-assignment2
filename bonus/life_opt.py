"""
conway.py 

A simple Python/matplotlib implementation of Conway's Game of Life.

Author: Mahesh Venkitachalam
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from functools import wraps

ON = 255
OFF = 0
vals = [ON, OFF]

fn_exec_time = []

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N * N, p=[0.2, 0.8]).reshape(N, N)


def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255], [255, 0, 255], [0, 255, 255]])
    grid[i : i + 3, j : j + 3] = glider


def addGosperGliderGun(i, j, grid):
    """adds a Gosper Glider Gun with top left cell at (i, j)"""
    gun = np.zeros(11 * 38).reshape(11, 38)

    gun[5][1] = gun[5][2] = 255
    gun[6][1] = gun[6][2] = 255

    gun[3][13] = gun[3][14] = 255
    gun[4][12] = gun[4][16] = 255
    gun[5][11] = gun[5][17] = 255
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
    gun[7][11] = gun[7][17] = 255
    gun[8][12] = gun[8][16] = 255
    gun[9][13] = gun[9][14] = 255

    gun[1][25] = 255
    gun[2][23] = gun[2][25] = 255
    gun[3][21] = gun[3][22] = 255
    gun[4][21] = gun[4][22] = 255
    gun[5][21] = gun[5][22] = 255
    gun[6][23] = gun[6][25] = 255
    gun[7][25] = 255

    gun[3][35] = gun[3][36] = 255
    gun[4][35] = gun[4][36] = 255

    grid[i : i + 11, j : j + 38] = gun

"""Modified update function since turning off animation"""
def update(grid, N):
    # Copy grid since we require 8 neighbors for calculation
    # and we go line by line
    newGrid = grid.copy()

    # Create a toroidal grid using modulo arithmetic
    left = np.roll(grid, 1, axis=1)
    right = np.roll(grid, -1, axis=1)
    up = np.roll(grid, 1, axis=0)
    down = np.roll(grid, -1, axis=0)
    up_left = np.roll(left, 1, axis=0)
    up_right = np.roll(right, 1, axis=0)
    down_left = np.roll(left, -1, axis=0)
    down_right = np.roll(right, -1, axis=0)

    # Compute 8-neighbor sum
    total = (
        left + right + up + down +
        up_left + up_right + down_left + down_right
    ) / 255

    # apply Conway's rules
    live_cells = (grid == ON)
    newGrid[live_cells & ((total < 2) | (total > 3))] = OFF
    newGrid[~live_cells & (total == 3)] = ON

    return newGrid


# main() function
"""Modified main function to measure the execution times for different grid sizes"""
# @profile
def main(N):
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(
        description="Runs Conway's Game of Life simulation."
    )
    # add arguments
    # parser.add_argument("--grid-size", dest="N", required=False)
    parser.add_argument("--mov-file", dest="movfile", required=False)
    parser.add_argument("--interval", dest="interval", required=False)
    parser.add_argument("--glider", action="store_true", required=False)
    parser.add_argument("--gosper", action="store_true", required=False)
    args = parser.parse_args()

    # set grid size
    # N = 100
    # if args.N and int(args.N) > 8:
    #     N = int(args.N)

    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # declare grid
    grid = np.array([])
    # check if "glider" demo flag is specified
    if args.glider:
        grid = np.zeros(N * N).reshape(N, N)
        addGlider(1, 1, grid)
    elif args.gosper:
        grid = np.zeros(N * N).reshape(N, N)
        addGosperGliderGun(10, 10, grid)
    else:
        # populate grid with random on/off - more off than on
        grid = randomGrid(N)

    for _ in range(50):  # Perform calculations for 50 iterations (adjust as needed)
        grid = update(grid, N)

    # set up animation
    # fig, ax = plt.subplots()
    # img = ax.imshow(grid, interpolation="nearest")
    # ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
    #   frames = 10,
    #   interval=updateInterval,
    #   save_count=50)

    # # of frames?
    # set output file
    # if args.movfile:
    #     ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])
        # pass

    # plt.show()


# call main
    
#Task 2
# if __name__ == "__main__":
#     #Executing for grid sizes 20-100 with a step of 2 for 100 iterations
#     for i, grid_size in enumerate(range(20, 201, 2), start=0):
#         fn_exec_time.append([])        #creating a lsit of lists
#         print(f"Executing for grid size equal to {grid_size}")
#         for x in range(10):
#             t1 = time.time()
#             main(grid_size)
#             t2 = time.time()
#             fn_exec_time[i].append(t2 - t1)


#     avg_exec_time_grid = []

#     #Calculating the average execution time for each grid size
#     for x in range (len(fn_exec_time)):
#         avg_exec_time_grid.append(1000*sum(fn_exec_time[x])/len(fn_exec_time[x]))
#         # print(f"Average execution time with grid size equal to {20 + 2*x} is {avg_exec_time_grid[x]} milliseconds")

#     #Plotting the information for various grid sizes
        
#     grid_sizes = [20 + 2 * i for i in range(len(avg_exec_time_grid))]
#     plt.plot(grid_sizes, avg_exec_time_grid, marker='.', linestyle='-')
#     plt.xlabel('Grid size')
#     plt.ylabel('Execution time (ms)')
#     plt.title('Execution time for various grid sizes')
#     plt.grid(True)
#     plt.show()
    
if __name__ == "__main__":
    #Grid size = 100 is the default value
    main(100)