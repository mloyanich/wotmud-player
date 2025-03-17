# main.py

import asyncio
import json
import logging
import os
import random
from mud_client import MUDClient  # Import the MUDClient class
from room import Room  # Import the Room class
from constants import APPLICATION_NAME
from utils import setup_logging

setup_logging()
module_logger = logging.getLogger(f"{APPLICATION_NAME}")

# File to store room data
ROOMS_FILE = "rooms.json"
# File to store the stack for the next run
STACK_FILE = "stack.json"
# Maximum number of rooms to visit
MAX_ROOMS = 2


def load_rooms():
    """Load the room dataset from the JSON file."""
    if os.path.exists(ROOMS_FILE):
        with open(ROOMS_FILE, "r") as file:
            return json.load(file)
    return []


def save_rooms(rooms):
    """Save the room dataset to the JSON file."""
    with open(ROOMS_FILE, "w") as file:
        json.dump(rooms, file, indent=2)


def load_stack():
    """Load the stack from the JSON file."""
    if os.path.exists(STACK_FILE):
        with open(STACK_FILE, "r") as file:
            return json.load(file)
    return []


def save_stack(stack):
    """Save the stack to the JSON file."""
    with open(STACK_FILE, "w") as file:
        json.dump(stack, file, indent=2)


async def get_current_room(client):
    """Get the room description and exits by calling 'look' and 'exits' commands."""
    # Send the 'look' command and read the output
    look_output = await client.send_and_read("look")

    # Send the 'exits' command and read the output
    exits_output = await client.send_and_read("exits")

    # Create a Room object with the combined output
    room = Room(look_output, exits_output)

    return room


async def travel_rooms(client):
    """Travel around the rooms, building a graph of connected rooms."""
    # Load the existing room dataset
    rooms = load_rooms()
    room_data = {room["id"]: room for room in rooms}  # Map room IDs to room data

    # Load the stack from the previous run (if it exists)
    path_stack = load_stack()

    # Counter for the number of rooms visited
    rooms_visited = 0

    # Get the current room description
    room = await get_current_room(client)
    print(room)  # Print the room description and exits

    # Check if the current room matches the top of the stack
    if path_stack and room.id != path_stack[-1]:
        print("Current room does not match the top of the stack. Resetting stack.")
        path_stack = []  # Reset the stack

    # Check if the room is already in the dataset
    if room.id not in room_data:
        # Add the new room to the dataset
        room_data[room.id] = {
            "id": room.id,
            "description": room.description,
            "raw_look_output": room.raw_look_output,
            "exits": {},  # Map of direction: room_id
        }
        print(f"New room added with ID: {room.id}")
    else:
        print(f"Room already exists with ID: {room.id}")

    # Push the current room to the path stack
    path_stack.append(room.id)

    # Travel to random exits until all reachable rooms are explored or MAX_ROOMS is reached
    while path_stack and rooms_visited < MAX_ROOMS:
        # Get the current room ID
        current_room_id = path_stack[-1]
        current_room = room_data[current_room_id]

        # Get the current room's exits
        exits = current_room.get("exits", {})
        untraversed_exits = [exit for exit in room.exits if exit not in exits]

        if untraversed_exits:
            # Choose a random untraversed exit
            chosen_exit = random.choice(untraversed_exits)
            print(f"Traveling to exit: {chosen_exit}")

            # Send the command to travel to the chosen exit
            await client.send_and_read(
                chosen_exit.lower()
            )  # Ensure the command is lowercase

            # Get the new room description
            new_room = await get_current_room(client)
            print(new_room)  # Print the room description and exits

            # Check if the new room is already in the dataset
            if new_room.id not in room_data:
                # Add the new room to the dataset
                room_data[new_room.id] = {
                    "id": new_room.id,
                    "description": new_room.description,
                    "raw_look_output": new_room.raw_look_output,
                    "exits": {},  # Map of direction: room_id
                }
                print(f"New room added with ID: {new_room.id}")
            else:
                print(f"Room already exists with ID: {new_room.id}")

            # Map the exit to the new room's ID
            room_data[current_room_id]["exits"][chosen_exit] = new_room.id

            # Push the new room to the path stack
            path_stack.append(new_room.id)

            # Increment the rooms visited counter
            rooms_visited += 1
        else:
            # No untraversed exits left in the current room
            print("No untraversed exits left. Backtracking.")
            path_stack.pop()  # Backtrack to the previous room

    # Save the updated room dataset
    save_rooms(list(room_data.values()))
    print(f"Room dataset saved to {ROOMS_FILE}")

    # Save the stack for the next run
    save_stack(path_stack)
    print(f"Stack saved to {STACK_FILE}")

    # Print the number of rooms visited
    print(f"Rooms visited: {rooms_visited}")


async def main():
    # Create the MUD client with debug logging
    client = MUDClient(log_level=logging.INFO)

    try:
        # Connect to the server
        await client.connect()

        # Login with credentials
        await client.login()
        first_message = await client.send_and_read("look")
        print(first_message)
        # Start traveling around the rooms
        await travel_rooms(client)

    except Exception as e:
        module_logger.error("An error occurred: %s", e)  # Lazy formatting
        raise e
    finally:
        # Close the connection
        await client.close()


# Run the MUD client
if __name__ == "__main__":
    asyncio.run(main())
