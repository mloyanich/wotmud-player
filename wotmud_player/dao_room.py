import json
import os

from pathlib import Path


class DAORoom:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DAORoom, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Load the JSON file when the singleton is first created."""
        # Get the rooms.json file path
        parent_dir = Path(__file__).parent.parent
        self._data_file = parent_dir / "rooms.json"
        self._rooms = self._load_data()

    def _load_data(self):
        """Load room data from the JSON file."""
        if not os.path.exists(self._data_file):
            raise FileNotFoundError(f"The file {self._data_file} does not exist.")

        with open(self._data_file, "r") as file:
            all_rooms = json.load(file)
        return {
            r_id: r_data
            for r_id, r_data in all_rooms.items()
            if not r_id.startswith("black_")
        }

    def get_all_rooms(self):
        """Return all rooms as a dictionary."""
        return self._rooms

    def get_room_by_id(self, room_id):
        """Return a room by its ID."""
        return self._rooms.get(str(room_id))  # Convert room_id to string for lookup

    def add_room(self, room):
        """Add a new room to the data and save it to the JSON file."""
        room_id = str(room["id"])  # Use the room ID as the key
        if room_id in self._rooms:
            print(f"Room with ID {room_id} already exists.")
            return
        self._rooms[room_id] = room
        self._save_data()

    def update_room(self, room_id, updated_data):
        """Update a room by its ID."""
        room_id = str(room_id)  # Convert room_id to string
        if room_id not in self._rooms:
            raise KeyError(f"Room with ID {room_id} does not exist.")
        self._rooms[room_id].update(updated_data)
        self._save_data()

    def delete_room(self, room_id):
        """Delete a room by its ID."""
        room_id = str(room_id)  # Convert room_id to string
        if room_id not in self._rooms:
            raise KeyError(f"Room with ID {room_id} does not exist.")
        del self._rooms[room_id]
        self._save_data()

    def _save_data(self):
        """Save the updated room data back to the JSON file."""
        with open(self._data_file, "w") as file:
            json.dump(self._rooms, file, indent=4)

    def to_dict(self):
        return self._rooms


# Example usage
if __name__ == "__main__":
    # Get all rooms
    room_dao = DAORoom()
    all_rooms = room_dao.get_all_rooms()
    print("All Rooms:", all_rooms)

    # Get a room by ID
    room = room_dao.get_room_by_id(1)
    print("Room with ID 1:", room)
