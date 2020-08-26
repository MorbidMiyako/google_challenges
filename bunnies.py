"""
You have maps of parts of the space station, each starting at a prison exit and ending at the door to an escape pod. The map is represented as a matrix of 0s and 1s, where 0s are passable space and 1s are impassable walls. The door out of the prison is at the top left (0,0) and the door into an escape pod is at the bottom right (w−1,h−1).

Write a function answer(map) that generates the length of the shortest path from the prison door to the escape pod, where you are allowed to remove one wall as part of your remodeling plans. The path length is the total number of nodes you pass through, counting both the entrance and exit nodes. The starting and ending positions are always passable (0). The map will always be solvable, though you may or may not need to remove a wall. The height and width of the map can be from 2 to 20. Moves can only be made in cardinal directions; no diagonal moves are allowed.

Test cases
Input:

maze = [[0, 1, 1, 0], 
        [0, 0, 0, 1], 
        [1, 1, 0, 0], 
        [1, 1, 1, 0]]
Output:

7
Input:

maze = [[0, 0, 0, 0, 0, 0], 
        [1, 1, 1, 1, 1, 0], 
        [0, 0, 0, 0, 0, 0], 
        [0, 1, 1, 1, 1, 1], 
        [0, 1, 1, 1, 1, 1], 
        [0, 0, 0, 0, 0, 0]]
Output:

11
"""
import copy


def solution(matrix):
    class Queue():
        def __init__(self):
            self.queue = []

        def enqueue(self, value):
            self.queue.append(value)

        def dequeue(self):
            if self.size() > 0:
                return self.queue.pop(0)
            else:
                return None

        def size(self):
            return len(self.queue)

    def get_neighbors(i, j, matrix, walls, wall_break, last_direction):
        # direction prevents going back, just bumps up efficiency

        moves_array = []

        # check if going up is open or not
        if last_direction != "down" and i != walls[0] and matrix[i-1][j] == 0:
            moves_array.append([False, [i-1, j], "up"])

        # if wall then try breaking it
        elif last_direction != "down" and i != walls[0] and break_wall(i-1, j, matrix, walls, "up") and wall_break is False:
            moves_array.append([True, [i-1, j], "up"])

        if last_direction != "up" and i != walls[1] and matrix[i+1][j] == 0:
            moves_array.append([False, [i+1, j], "down"])

        elif last_direction != "up" and i != walls[1] and break_wall(i+1, j, matrix, walls, "down") and wall_break is False:
            moves_array.append([True, [i+1, j], "down"])

        if last_direction != "right" and j != walls[2] and matrix[i][j-1] == 0:
            moves_array.append([False, [i, j-1], "left"])

        elif last_direction != "right" and j != walls[2] and break_wall(i, j-1, matrix, walls, "left") and wall_break is False:
            moves_array.append([True, [i, j-1], "left"])

        if last_direction != "left" and j != walls[3] and matrix[i][j+1] == 0:
            moves_array.append([False, [i, j+1], "right"])

        elif last_direction != "left" and j != walls[3] and break_wall(i, j+1, matrix, walls, "right") and wall_break is False:
            moves_array.append([True, [i, j+1], "right"])

        return moves_array

    def break_wall(i, j, matrix, walls, last_direction):
        # direction eliminates thinking a skip has been made when one just finds the open space we came from
        wall_break = False

        # checks if after breaking a wall, there is a new open space
        if last_direction != "down" and i != walls[0] and matrix[i-1][j] == 0:
            wall_break = True

        elif last_direction != "up" and i != walls[1] and matrix[i+1][j] == 0:
            wall_break = True

        elif last_direction != "right" and j != walls[2] and matrix[i][j-1] == 0:
            wall_break = True

        elif last_direction != "left" and j != walls[3] and matrix[i][j+1] == 0:
            wall_break = True

        return wall_break

    def bfs(matrix):

        # starting coordinates, always bottom left
        i = len(matrix) - 1
        j = len(matrix[0]) - 1

        # creates starting queue
        queue = Queue()
        queue.enqueue([False, [[i, j]], "north"])
        walls = [0, len(matrix)-1, 0, len(matrix[0])-1]

        # realised that a matrix with tons of 0's created too many branches, and a single visited didnt work
        # since a coordinate could be visited early by breaking a wall
        # just splite the two dicts up, and works much better now
        false_visited = {}
        true_visited = {}

        # if queue runs out, then we have a problem
        while queue.size() > 0:

            # get the first added path
            path = queue.dequeue()

            # first element is the coordinate
            visiting_coordinate = path[1][-1]

            # keeps track of if a wall was broken
            wall_break = path[0]

            # keeps track of the most recent moved direction
            last_direction = path[2]

            if wall_break:

                if str(visiting_coordinate) not in true_visited:

                    true_visited[str(visiting_coordinate)
                                 ] = visiting_coordinate

                    # final solution, first solution to arrive using breath first is the minimum lenght
                    if visiting_coordinate[0] == 0 and visiting_coordinate[1] == 0:
                        return path

                    # get the different optional next coordinates, and register if a wall break was needed
                    for next_visiting in get_neighbors(visiting_coordinate[0], visiting_coordinate[1], matrix, walls, wall_break, last_direction):

                        # due to nested array a deep copy is required
                        path_copy = copy.deepcopy(path)

                        # toggles if a wall has been broken
                        if next_visiting[0]:
                            path_copy[0] = True

                        # adds next coordinate
                        path_copy[1].append(next_visiting[1])

                        # adds last direction
                        path_copy[2] = next_visiting[2]

                        # enqueues whole
                        queue.enqueue(path_copy)

            else:

                if str(visiting_coordinate) not in false_visited:

                    false_visited[str(visiting_coordinate)
                                  ] = visiting_coordinate

                    # final solution, first solution to arrive using breath first is the minimum lenght
                    if visiting_coordinate[0] == 0 and visiting_coordinate[1] == 0:
                        return path

                    # get the different optional next coordinates, and register if a wall break was needed
                    for next_visiting in get_neighbors(visiting_coordinate[0], visiting_coordinate[1], matrix, walls, wall_break, last_direction):

                        # due to nested array a deep copy is required
                        path_copy = copy.deepcopy(path)

                        # toggles if a wall has been broken
                        if next_visiting[0]:
                            path_copy[0] = True

                        # adds next coordinate
                        path_copy[1].append(next_visiting[1])

                        # adds last direction
                        path_copy[2] = next_visiting[2]

                        # enqueues whole
                        queue.enqueue(path_copy)

        return "Error"

    # runs bfs
    complete_path = bfs(matrix)

    # returns the desired information
    return len(complete_path[1])


# print(solution([
#     [0, 1, 0, 1, 0, 0, 0],
#     [0, 0, 0, 1, 0, 1, 0]
# ]))

# print(solution([[0, 0], [1, 1], [0, 0]]))

print(solution([[0, 0, 0, 0, 0],
                [1, 0, 1, 1, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 1, 0, 1],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0]]))

print(solution([[0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0],
                [1, 1, 0, 1, 1, 1],
                [0, 1, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 0]]))

print(solution([[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
                ]))

print(solution([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]))

# print(solution([[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                 [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#                 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                 [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                 [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                 [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
#                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))
