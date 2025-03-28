import json
import os

from mud_room import Room


class MUDMap:
    def __init__(self, rooms_file="rooms.json", map_file="map.json"):
        self.map_file = map_file
        self.map = self.load_map()
        self.rooms_file = rooms_file
        self.rooms = self.load_rooms()

    def load_map(self):
        """Load the map from the JSON file."""
        if os.path.exists(self.map_file):
            with open(self.map_file, "r", encoding="utf-8") as file:
                rooms_data = json.load(file)
                return {
                    room["id"]: Room.from_dict(room)
                    for room in rooms_data
                    if not room["id"].startswith("black_")
                }
        else:
            return {}

    def load_rooms(self):
        """Load the room dataset from the JSON file."""
        if os.path.exists(self.rooms_file):
            with open(self.rooms_file, "r", encoding="utf-8") as file:
                rooms_data = json.load(file)
                return {room["id"]: Room.from_dict(room) for room in rooms_data}
        else:
            return {}

    def save_rooms(self):
        """Save the room dataset to the JSON file."""
        with open(self.rooms_file, "w", encoding="utf-8") as file:
            json.dump(list(self.rooms.values()), file, indent=2)

    def save_map(self):
        """Save the map to the JSON file."""
        with open(self.map_file, "w", encoding="utf-8") as file:
            json.dump([room.to_dict() for room in self.map.values()], file, indent=2)

    def add_room(self, room: Room):
        """
        Add a new room to the map.
        :param room: A Room object or dictionary containing room data.
        """
        if room.id not in self.rooms:
            self.rooms[room.id] = room.to_dict()
            print(f"New room added with ID: {room.id}")
        else:
            print(f"Room already exists with ID: {room.id}")

    def get_room(self, room_id):
        """
        Retrieve a room by its ID.
        :param room_id: The ID of the room to retrieve.
        :return: The room data as a dictionary, or None if not found.
        """
        return self.rooms.get(room_id, None)

    def connect_rooms(self, room_from_id, exit_direction, room_to_id):
        """
        Update the exits of a room.
        :param room_from_id: The ID of the room to update.
        :param exit_direction: The direction of the exit (e.g., "N", "S").
        :param room_to_id: The ID of the room the exit leads to.
        """
        room_from = self.get_room(room_from_id)
        room_to = self.get_room(room_to_id)
        if not room_from or not room_to:
            print("both rooms should exist on the map. not updating")
        room_from.map_path(exit, room_to)
        opposite_direction = self.get_opposite(exit_direction)
        room_to.map_path(opposite_direction, room_from)

    def get_opposite(self, direction):
        """
        Get the opposite direction of the specified direction.
        :param direction: The direction to find the opposite of.
        :return: The opposite direction.
        """
        opposites = {"N": "S", "S": "N", "E": "W", "W": "E"}
        return opposites.get(direction, None)
