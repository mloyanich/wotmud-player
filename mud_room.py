"""
mud_room module, that contains the Room class for representing a room in a MUD environment
along with a bit of code to test it.
"""

import hashlib
import re
import uuid
import json
from mud_room_features import RoomFeatures


class Room:
    """
    Represents a room in a MUD (Multi-User Dungeon) environment.

    A Room object is initialized with a look output and an exits output.
    It extracts room features and exits from these inputs and generates a unique room ID.
    """

    def __init__(self, look_output, exits_output):
        """
        Initialize the Room with the output of the 'look' and 'exits' commands.

        Args:
            look_output (str): The descriptive output from the 'look' command.
            exits_output (str): The output from the 'exits' command, listing available exits.
        """
        self.raw_look_output = look_output
        self.features = self._extract_features()
        self.id = self._generate_id()
        self.raw_exits_output = exits_output
        self.exits = self._extract_exits()

    def _extract_features(self):
        """
        Extract features from the look output using the RoomFeatures class.

        Returns:
            RoomFeatures: An object representing the room's features.
        """
        return RoomFeatures(self.raw_look_output)

    def _extract_exits(self):
        """
        Extract the room exits from the 'exits' output using regex matching.

        Expects the exits output to be in the format:
        "North - Description\nWest - Description\n"

        Returns:
            dict: A dictionary mapping exit directions to their descriptions and connected room.
                  Example:
                  {
                      'N': {'description': 'Grand Corridor', 'room': None},
                      'W': {'description': 'Kitchen', 'room': None}
                  }
        """
        exit_regex = re.compile(r"(North|South|East|West|Up|Down)\s*-\s*([^\n,]+)")
        matches = exit_regex.findall(self.raw_exits_output)
        exits_dict = {
            direction[0].upper(): {"description": description, "room": None}
            for direction, description in matches
        }

        return exits_dict

    def _generate_id(self):
        """
        Generate a unique ID for the room based on its features.

        If the look output indicates that the room is pitch black,
        generate a unique ID using a UUID. Otherwise, generate an MD5 hash
        of the room's features string representation.

        Returns:
            str: A unique identifier for the room.
        """
        if self.raw_look_output == "It is pitch black...":
            print("It is pitch black...")
            return str(f"black_{uuid.uuid4()}")
        return hashlib.md5(str(self.features).encode("utf-8")).hexdigest()

    def map_room_to_exit(self, direction, room):
        """
        Map a Room object to a specific exit direction.

        Args:
            direction (str): The exit direction (e.g., 'N' for North).
            room (Room): The Room object to map to the exit.

        Raises:
            ValueError: If the specified direction is not a valid exit.
        """
        direction_key = direction[0].upper()
        if direction_key in self.exits:
            self.exits[direction_key]["room"] = room
        else:
            raise ValueError(f"Invalid exit direction: {direction}")

    def _exits_to_dict(self):
        """
        Convert the exits to a dictionary format.

        The connected room objects are replaced with their IDs.

        Returns:
            dict: A dictionary mapping exit directions to their descriptions and room IDs.
                  Example:
                  {
                      'N': {'description': 'Grand Corridor', 'room_id': '123abc'},
                      'W': {'description': 'Kitchen', 'room_id': None}
                  }
        """
        return {
            direction: {
                "description": data["description"],
                "room_id": data["room"].id if data["room"] else None,
            }
            for direction, data in self.exits.items()
        }

    def to_dict(self):
        """
        Convert the Room object to a dictionary.

        The dictionary includes the room ID, features, raw output data, and exits.

        Returns:
            dict: A dictionary representation of the room.
                  Example:
                  {
                      'id': '123abc',
                      'features': {...},
                      'raw_look_output': 'You are in a room...',
                      'raw_exits_output': 'Exits...',
                      'exits': {
                          'N': {'description': 'Grand Corridor', 'room_id': '123abc'},
                          'W': {'description': 'Kitchen', 'room_id': None}
                      }
                  }
        """
        return {
            "id": self.id,
            "features": self.features.to_dict(),
            "raw_look_output": self.raw_look_output,
            "raw_exits_output": self.raw_exits_output,
            "exits": self._exits_to_dict(),
        }

    def __str__(self):
        """
        Return a formatted string representation of the room.

        Includes the room's features and exits.

        Returns:
            str: A formatted string representation of the room.
                  Example:
                  "Features:
                   - Marble pillars
                   - Golden chandelier

                   Exits:
                   N - Grand Corridor
                   W - Kitchen"
        """
        description_str = f"Features:\n{self.features}"
        exits_str = "Exits:\n" + "\n".join(
            [
                f"{direction} - {data['description']}"
                for direction, data in self.exits.items()
            ]
        )
        return f"{description_str}\n\n{exits_str}"


if __name__ == "__main__":
    # Example usage
    LOOK_OUTPUT = "\u001b[36mCrown and Lion Tavern\u001b[0m\r\n..."
    EXITS_OUTPUT = "Obvious exits:\nNorth - A Dilapidated Shop\nWest - A Dark Alley\n"
    parsed_room = Room(LOOK_OUTPUT, EXITS_OUTPUT)
    print(parsed_room)
    print(json.dumps(parsed_room.to_dict(), indent=4))
    parsed_room.map_room_to_exit(
        "N", Room("Another room", "Obvious exits:\nSouth - Tavern\n")
    )
    print(parsed_room)
    print(json.dumps(parsed_room.to_dict(), indent=4))
