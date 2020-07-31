# for graphics purposes
import matplotlib.pyplot as plt
#import time  # for preventing program end when plotting the maze
# RNG stuff
import random


def draw_maze():
    # for plotting the initial maze, with all of the initial walls
    for key, value in Wall_dict.items():
        x_pos = [value.A[0], value.B[0]]
        y_pos = [value.A[1], value.B[1]]
        value.id, = ax.plot(x_pos, y_pos, 'k', linewidth=1)

    ## updates matplotlib figure
    ## these commands are reqired to keep the figure from pausing the script
    ## comment out these lines to instant create the mazes
    # plt.ion()
    # plt.draw()
    # plt.pause(0.001)


class Cursor:
    def __init__(self, pos, dir):
        # simple error checking if the pos or dir aren't given as tuples
        if isinstance(pos, tuple) is False or isinstance(dir, tuple) is False:
            print("cursor position and direction must be tuple")
        self.pos = pos
        self.dir = dir

    def move(self):
        # keep record of children and parent cells
        old_pos = self.pos
        self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
        Cell_dict[self.pos].parent = old_pos
        Cell_dict[self.pos].child = self.pos
        # time.sleep(2)

        # delete wall between old position and new
        if self.dir == (0, 1):  # up
            Cell_dict[self.pos].wall_down.delete()
        elif self.dir == (0, -1):  # down
            Cell_dict[self.pos].wall_up.delete()
        elif self.dir == (1, 0):  # right
            Cell_dict[self.pos].wall_left.delete()
        elif self.dir == (-1, 0):  # left
            Cell_dict[self.pos].wall_right.delete()
        else:
            print("error in cursor.move")
            exit()

    def rand_dir(self):
        new_adjacent = Cell_dict[self.pos].adjacent_cell_list
        # cull  visited cells by creating new list.
        # Deleting fro original cell would cause the cursor to sometimes backtrack
        adjacent = []
        for i in new_adjacent:
            visit = i.visited
            if i.visited == False:
                adjacent.append(i)
        # check for number of adjacent cells
        if len(adjacent) == 0:
            # print("No possible moves, revert back to latest point with valid moves")
            return 1
        # don't want bracnching directly from end cell
        elif self.pos == end:
            # print("End cell, revert")
            return 1
        else:
            next_cell = random.choice(adjacent)
            if next_cell.visited == True:
                print("Trying to visit already visited cell", next_cell.pos)
                # time.sleep(10)
                exit()
            self.dir = ((next_cell.pos[0] - self.pos[0]), (next_cell.pos[1] - self.pos[1]))
            return 0

    # draw the cursor
    # purely for aesthetic purposes
    def draw(self):
        circle1 = plt.Circle((self.pos[0] + 0.5, self.pos[1] + 0.5), 0.4)
        plt.gcf().gca().add_artist(circle1)
        ### comment out these lines to instant create the mazes
        # plt.ion()
        # plt.draw()
        # plt.pause(0.001)


class Cell:
    def __init__(self, pos):
        if isinstance(pos, tuple) is False:
            print("Cell position must be tuple")
        self.pos = pos
        # link walls to the cell
        self.wall_left = Wall_dict[(self.pos[0], self.pos[1], self.pos[0], self.pos[1] + 1)]
        self.wall_right = Wall_dict[(self.pos[0] + 1, self.pos[1], self.pos[0] + 1, self.pos[1] + 1)]
        self.wall_up = Wall_dict[(self.pos[0], self.pos[1] + 1, self.pos[0] + 1, self.pos[1] + 1)]
        self.wall_down = Wall_dict[(self.pos[0], self.pos[1], self.pos[0] + 1, self.pos[1])]

        # child and parent information for storing valid moves in the maze
        self.child = ()
        self.parent = ()

        # has the cell been visited in the maze/integrated into the maze
        self.visited = False
        # list of adjacent cells
        self.adjacent_cell_list = []

    def init_cell_links(self):
        # link the adjacent cells to this cell
        if self.pos[0] != 0:
            self.cell_left = Cell_dict[(self.pos[0] - 1, self.pos[1])]
            self.adjacent_cell_list.append(self.cell_left)
        if self.pos[0] != Maze_size - 1:
            self.cell_right = Cell_dict[(self.pos[0] + 1, self.pos[1])]
            self.adjacent_cell_list.append(self.cell_right)
        if self.pos[1] != Maze_size - 1:
            self.cell_up = Cell_dict[(self.pos[0], self.pos[1] + 1)]
            self.adjacent_cell_list.append(self.cell_up)
        if self.pos[1] != 0:
            self.cell_down = Cell_dict[(self.pos[0], self.pos[1] - 1)]
            self.adjacent_cell_list.append(self.cell_down)


class Wall:
    def __init__(self, A, B):
        if isinstance(A, tuple) is False or isinstance(B, tuple) is False:
            print("A or B are not tuples")
            exit(1)
        self.A = A  # wall vertex A
        self.B = B  # wall vertex B
        self.exist = True

    def delete(self):
        self.id.set_linestyle('None')  # allows one to get rid of a specific line object (won't need to be drawn)
        self.exist = False

        ### comment out these lines to instant create the mazes
        # plt.ion()
        # plt.draw()
        # plt.pause(0.001)

# for the making of multiple mazes
for i in range(10):

    Maze_size = 20
    Wall_dict = {}
    # initialize grid with wall objects, stored in a dictionary
    for y in range(Maze_size):
        for x in range(Maze_size):
            # horizontal bar
            A_hor = (x, y)
            B_hor = (x + 1, y)
            # vertical bar
            A_vert = (x, y)
            B_vert = (x, y + 1)

            Wall_dict[(A_hor[0], A_hor[1], B_hor[0], B_hor[1])] = Wall(A_hor, B_hor)
            Wall_dict[(A_vert[0], A_vert[1], B_vert[0], B_vert[1])] = Wall(A_vert, B_vert)
        # extra vertical bar at end of each row
        A_vert = (Maze_size, y)
        B_vert = (Maze_size, y + 1)
        Wall_dict[(A_vert[0], A_vert[1], B_vert[0], B_vert[1])] = Wall(A_vert, B_vert)
    # extra horizontal bar at base of each row
    for x in range(Maze_size):
        # horizontal bar
        A_hor = (x, Maze_size)
        B_hor = (x + 1, Maze_size)

        Wall_dict[(A_hor[0], A_hor[1], B_hor[0], B_hor[1])] = Wall(A_hor, B_hor)

    # check size of wall dictionary. Should be equal to 2*n^2+2n
    Wall_dict_size = len(Wall_dict)
    Check_size = 2 * Maze_size ** 2 + 2 * Maze_size
    if Wall_dict_size != Check_size:
        print("Wall Dictionary missing entry")
        print(Wall_dict_size)
        print(Check_size)
        exit(1)

    # initialize "plotting" Window
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_aspect(1)  # set aspect ratio to 1
    ax.set_axis_off()
    fig.add_axes(ax)

    # draw the initial maze
    draw_maze()

    # Initializes, maze dictionary, containing objects of the maze size
    Cell_dict = {}
    for y in range(Maze_size):
        for x in range(Maze_size):
            Cell_dict[(x, y)] = Cell((x, y))
    for key in Cell_dict:
        Cell_dict[key].init_cell_links()

    # start building the maze

    # start and end points for the maze
    start = (0, Maze_size - 1)
    end = (Maze_size - 1, 0)
    Cell_dict[start].wall_left.delete()
    Cell_dict[end].wall_right.delete()

    # time.sleep(10)

    Maker = Cursor(start, (1, 0))
    # Maker.draw() #draws the "cursor position, if one is watching the maze be made
    Cell_dict[Maker.pos].visited = True
    Visited = 1
    while Visited < (Maze_size ** 2):
        revert = Maker.rand_dir()
        if revert == 1:
            # print(Cell_dict[Maker.pos].pos)
            # temp = Cell_dict[Maker.pos]
            if Maker.pos != start:
                Maker.pos = Cell_dict[Cell_dict[Maker.pos].parent].pos
        else:
            Maker.move()
            Cell_dict[Maker.pos].visited = True
            Visited = Visited + 1
            # Maker.draw()
            # time.sleep(0.001)
print("Maze(s) Made")
# time.sleep(100)

# keeps plots from closing at the termination of the scripts
plt.ioff()
plt.show()
