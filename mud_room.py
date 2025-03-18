import hashlib
import re
import uuid
import json
from mud_room_features import RoomFeatures


class Room:
    def __init__(self, look_output, exits_output):
        """Initialize the Room with the output of the 'look' and 'exits' commands."""
        self.raw_look_output = look_output
        self.features = self._extract_features()
        self.id = self._generate_id()
        self.raw_exits_output = exits_output
        self.exits = self._extract_exits()

    def _extract_features(self):
        return RoomFeatures(self.raw_look_output)

    def _extract_exits(self):
        """Extract the room exits from the 'exits' output."""
        exit_regex = re.compile(r"(North|South|East|West|Up|Down)\s*-\s*([^\n,]+)")
        matches = exit_regex.findall(self.raw_exits_output)
        exits_dict = {
            direction[0].upper(): {"description": description, "room": None}
            for direction, description in matches
        }

        return exits_dict

    def _generate_id(self):
        """Generate a unique ID for the room using its description."""
        # Use MD5 hash of the description to generate a unique ID
        if self.raw_look_output == "It is pitch black...":
            print("It is pitch black...")
            return str(f"black_{uuid.uuid4()}")
        return hashlib.md5(str(self.features).encode("utf-8")).hexdigest()

    def map_room_to_exit(self, direction, room):
        """
        Maps a room object to a specific exit direction.

        Args:
            direction (str): The exit direction (e.g., 'N').
            room (Room): The Room object to map to the exit.
        """
        # Convert the direction to uppercase first character for consistency
        direction_key = direction[0].upper()
        if direction_key in self.exits:
            self.exits[direction_key]["room"] = room
        else:
            raise ValueError(f"Invalid exit direction: {direction}")

    def _exits_to_dict(self):
        """
        Generates a dictionary representation of the exits with room_id instead of the Room object.

        Returns:
            dict: A dictionary mapping exit directions to their descriptions and room_id.
        """
        return {
            direction: {
                "description": data["description"],
                "room_id": data["room"].id if data["room"] else None,
            }
            for direction, data in self.exits.items()
        }

    def to_dict(self):
        """Convert the room data to a dictionary."""
        return {
            "id": self.id,
            "features": self.features.to_dict(),
            "raw_look_output": self.raw_look_output,
            "raw_exits_output": self.raw_exits_output,
            "exits": self._exits_to_dict(),
        }

    def __str__(self):
        """Return a formatted string representation of the room."""
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
