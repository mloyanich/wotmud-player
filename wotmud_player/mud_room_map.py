import json

from wotmud_player.mud_room import Room
from wotmud_player.utils import setup_logging


class RoomMap(Room):
    """
    A subclass of Room that provides a simplified dictionary representation
    and string formatting for mapping connected rooms.

    Inherits from:
        Room: The base class representing a room.
    """

    def to_dict(self):
        """
        Convert the RoomMap object to a dictionary format.

        The dictionary maps the room's ID to its exits, where connected rooms
        are represented by their IDs.

        Returns:
            dict: A dictionary mapping the room's ID to its exits.
                  Example:
                  {
                      '123abc': {
                          'N': '456def',
                          'W': None
                      }
                  }
        """
        return {
            self.id: self._exits_to_dict(),
        }

    def __str__(self):
        """
        Return a formatted string representation of the room and its exits.

        Each exit is shown with the connected room's ID or None if not connected.

        Returns:
            str: A formatted string representing the room's ID and exits.
                  Example:
                  "ID: 123abc
                  Exits:
                  N: 456def
                  W: None"
        """
        return f"ID: {self.id}\n{self._exits_str()}"

    def map_room_to_exit(self, direction, room_id):
        if not direction or direction not in self.exit_map:
            raise ValueError(f"Invalid exit direction: {direction}")
        self.exits[direction] = room_id

    exit_map = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}

    def _opposite_exit(self, direction):
        return self.exit_map.get(direction.upper(), None)

    def map_room_to_opposite_exit(self, direction, room_id):
        op = self._opposite_exit(direction)
        self.map_room_to_exit(op, room_id)


if __name__ == "__main__":
    logger = setup_logging(__name__)
    # Example usage
    LOOK_OUTPUT = "\u001b[36mCrown and Lion Tavern\u001b[0m\r\n..."
    EXITS_OUTPUT = "Obvious exits:\nNorth - A Dilapidated Shop\nWest - A Dark Alley\n"

    # Create a RoomMap object
    parsed_room = RoomMap(LOOK_OUTPUT, EXITS_OUTPUT)
    logger.info(parsed_room)
    logger.info(json.dumps(parsed_room.to_dict(), indent=4))

    # Connect another room to the north exit
    new_room = RoomMap("Another room", "Obvious exits:\nSouth - Tavern\n")
    parsed_room.map_room_to_exit("N", new_room.id)

    # Display updated room info
    logger.info(parsed_room)
    logger.info(json.dumps(parsed_room.to_dict(), indent=4))
    logger.info(new_room)
    new_room.map_room_to_opposite_exit("N", parsed_room.id)
    logger.info(new_room)
