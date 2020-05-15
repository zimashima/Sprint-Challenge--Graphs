from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def traverse(room, visited=None, path=None):
    
    opposite = { 'n':'s', 'e':'w', 's':'n', 'w':'e' }
    current_room_id = room.id

    if visited is None:
        visited = {}
    if path is None:
        path = []

    if len(visited) == len(room_graph):
        return path

    if current_room_id not in visited:
        visited[current_room_id] = {i:'?' for i in room.get_exits()}

    for direction in room.get_exits():
        if visited[current_room_id][direction] == '?':
            visited[current_room_id][direction] = room.get_room_in_direction(direction).id
            player.travel(direction)
            new_room = player.current_room
            if new_room.id not in visited:
                visited[new_room.id] = {i:'?' for i in room.get_exits()}
            visited[new_room.id][opposite[direction]] = current_room_id
            return traverse(new_room, visited, path)
    

traversal_path = traverse(world.starting_room)
print(traversal_path)

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




# UNCOMMENT TO WALK AROUND

# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
