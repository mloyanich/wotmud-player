# room.py

import hashlib
import re
import uuid
from mud_room_features import RoomFeatures


class Room:
    def __init__(self, look_output, exits_output):
        """Initialize the Room with the output of the 'look' and 'exits' commands."""
        self.raw_look_output = look_output
        self.features = self._extract_features(look_output)
        self.id = self._generate_id()
        self.raw_exits_output = exits_output
        self.exits = self._extract_exits()

    def _extract_features(self, look_output):
        return RoomFeatures(look_output)

    def _extract_exits(self):
        """Extract the room exits from the 'exits' output."""
        exits = []
        for line in self.raw_exits_output.splitlines():
            # Match lines like "North - A Dilapidated Shop"
            match = re.match(r"^\s*(\w+)\s*-\s*.*$", line)
            if match:
                direction = match.group(1)
                # Extract the first letter of the direction (e.g., "N" for "North")
                exits.append(direction[0].upper())
        return exits

    def _generate_id(self):
        """Generate a unique ID for the room using its description."""
        # Use MD5 hash of the description to generate a unique ID
        if self.raw_look_output == "It is pitch black...":
            print("It is pitch black...")
            return str(f"black_{uuid.uuid4()}")
        return hashlib.md5(str(self.features).encode("utf-8")).hexdigest()

    def to_dict(self):
        """Convert the room data to a dictionary."""
        return {
            "id": self.id,
            "features": self.features.get_features_with_color_names(),
            "raw_look_output": self.raw_look_output,
            "raw_exits_output": self.raw_exits_output,
            "exits": self.exits,
        }

    def __str__(self):
        """Return a formatted string representation of the room."""
        description_str = (
            f"Description:\n{self.features.get_features_with_color_names()}"
        )
        exits_str = "Exits:\n" + "\n".join(self.exits)
        return f"{description_str}\n\n{exits_str}"
