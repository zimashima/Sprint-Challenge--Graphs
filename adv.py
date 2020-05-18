from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

#My code

#my first attempt at the solution but decided not to use it for now
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


#my new attempt, try to approach it simpler way

current_room = player.current_room #assign current room

entries = {} #visited entries
entries[current_room.id] = { i:'?' for i in current_room.get_exits() }
#this should give { room_id: { 'n': '?', 's': '?', 'e': '?','w': '?' }

path = [] #backtrack tracker
opposite = { 'n':'s','s':'n','w':'e','e':'w' } #easy reference for opposite direction



#we want to keep looping until the number of loops are equal to the total number of rooms
while len(entries) < len(room_graph):

    # if current_room is not in entries, then we initialize it with all exits with '?'
    
    if current_room.id not in entries:
        entries[current_room.id] = { i:'?' for i in current_room.get_exits() }

        # check if current_room still has unexplored path, by seeing if '?' still exist in one of the key
            # if there is no unexplored path (no '?' in any direction key), we need to backtrack to the latest previous direction (path[-1])
            # then assigned the next_room.id to the direction entries in our entries dictionary 
                # to mark that the path is no longer '?' and is replaced by the id of respective room
            # then remove the latest previous direction in the backtrack path as we had just walked through it
            # then assign next_room to current_room and reset the while loop

        # ELSE
            # select the remaining direction key, and if it's '?' then execute the command to move into that direction
            # get what next_room is and assigned next_room id to that direction
                # if next room is not in the entries, then we need to initiate it in the entries before we move on
                # and assigned the value to the appropriate direction accordingly
                # current_room direction = next_room id, in the next_room entries, opposite[direction] = current_room id
            # regardless of the above...
            # also append the backtrack step and append path into traversal path
            # break it so that for loop wouldn't be repeat and it would allow us to continue traversing
            # then make next_room the current_room to reset the loop



    if '?' not in entries[current_room.id].values():
        next_room = current_room.get_room_in_direction(path[-1]) #get the room in the backtrack
        
        if next_room.id not in entries:
            entries[next_room.id] = { i:'?' for i in next_room.get_exits() }
        
        entries[current_room.id][path[-1]] = next_room.id #assign value just in case
        entries[next_room.id][opposite[path[-1]]] = current_room.id #assign value for the other room
        traversal_path.append(path[-1]) #add the backtrack step to the real path
        path = path[:-1] #remove the backtrack out
        current_room = next_room #reset that loop
    
    else:
        
        for direction in entries[current_room.id]:

            if entries[current_room.id][direction] == '?':
                next_room = current_room.get_room_in_direction(direction)

                if next_room.id not in entries:
                    entries[next_room.id] = { i:'?' for i in next_room.get_exits() }

                entries[current_room.id][direction] = next_room.id
                entries[next_room.id][opposite[direction]] = current_room.id
                current_room = next_room
                traversal_path.append(direction) #add the direction to the main path
                path.append(opposite[direction]) #append the backtrack in case if we need to backtrack
                
                break

        

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
