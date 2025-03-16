# room.py

import hashlib
import re
import uuid


class Room:
    def __init__(self, look_output, exits_output):
        """Initialize the Room with the output of the 'look' and 'exits' commands."""
        self.raw_look_output = look_output
        self.raw_exits_output = exits_output
        self.description = look_output
        self.exits = self._extract_exits()
        self.id = self._generate_id()

    def _extract_description(self):
        """Extract the room description from the 'look' output."""
        # The description is everything before the "[ obvious exits: * ]" line
        exits_match = re.search(r"\[ obvious exits: .* \]", self.raw_look_output)
        if exits_match:
            return self.raw_look_output[: exits_match.start()].strip()
        return self.raw_look_output.strip()

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
        if self.description == "It is pitch black...":
            print("It is pitch black...")
            return str(f"black_{uuid.uuid4()}")
        return hashlib.md5(self.description.encode("utf-8")).hexdigest()

    def to_dict(self):
        """Convert the room data to a dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "raw_look_output": self.raw_look_output,
            "raw_exits_output": self.raw_exits_output,
            "exits": self.exits,
        }

    def __str__(self):
        """Return a formatted string representation of the room."""
        description_str = f"Description:\n{self.description}"
        exits_str = "Exits:\n" + "\n".join(self.exits)
        return f"{description_str}\n\n{exits_str}"
