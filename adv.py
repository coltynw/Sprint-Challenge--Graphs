from room import Room
from player import Player
from world import World

import random
import time
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# lets not do this every single time I test
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


print(world)
# I think i'm gunna try to do all this in one while loop
# the hard part is understanding all these global variables right away

# player = created from the Player function run with the starting room from the world file passed in, this should start at room 0,0
# player.current_room = property of player we can check to see what room we are in
# player.starting room = parameter that = the initial current room
# player.travel = takes a direction and moves player and current room into the next room
# .direction = parameter of player.travel, room.connect_rooms and get_room_in_direction

# world = variable created from world class
# initial values = starting_room, rooms, room_grid, grid_size
# world class functions = load_graph and print_rooms

# traversal path = empty array variable, I have to use this so it is picked up in the tests lower in the file. I will put the order we visited in the nodes in here
# visited_rooms = set() I should use?

# coltyn made
# exits = ways out of the room you are in
# paths = ways to go in a stack
# path = next move
# v =  visited_rooms redefined
# end = next thing out of the paths stack
# move = direction we're current moving 



def dfs(direction): 
# return the room we came from
    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "e":
        return "w"
    elif direction == "w":
        return "e"

paths = [] #stack
v = set() # visted nodes/rooms

while len(v) < len(world.rooms): #while there are still unvisited rooms
    exits = player.current_room.get_exits()
    # print(player.current_room) 
    # time.sleep(0.3)
    # print('rooms visited:', len(v))
    path = []

    for i in exits: # look for a way to go
        if i is not None and player.current_room.get_room_in_direction(i) not in v:
            path.append(i) # add next room to path
            # print(path) 

    v.add(player.current_room) # put the room we're in into visited

    if len(path) != 0: # if we still have ways to go
        # randomly pick index of move
        move = random.randint(0, len(path) -1) 
        # add the move to paths
        paths.append(path[move])
        # actually move there
        player.travel(path[move])
        # add it to the history
        traversal_path.append(path[move])

    else: # if theres no ways to go
        # we want to restart the function from the current room
        # the room left in the stack is the dead end
        end = paths.pop() 
        # restart function
        player.travel(dfs(end)) 
        # and add to the history
        traversal_path.append(dfs(end))


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
