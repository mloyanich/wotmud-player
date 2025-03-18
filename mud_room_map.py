import json
from mud_room import Room


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

    def _exits_to_dict(self):
        """
        Generate a simplified dictionary representation of the room's exits.

        The connected rooms are represented by their IDs or None if not connected.

        Returns:
            dict: A dictionary mapping exit directions to connected room IDs.
                  Example:
                  {
                      'N': '456def',
                      'W': None
                  }
        """
        return {
            direction: data["room"].id if data["room"] else None
            for direction, data in self.exits.items()
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
        exits_str = "\n".join(
            [
                f"{direction}: {data['room'].id if data['room'] else None}"
                for direction, data in self.exits.items()
            ]
        )
        return f"ID: {self.id}\nExits: \n{exits_str}"


if __name__ == "__main__":
    # Example usage
    LOOK_OUTPUT = "\u001b[36mCrown and Lion Tavern\u001b[0m\r\n..."
    EXITS_OUTPUT = "Obvious exits:\nNorth - A Dilapidated Shop\nWest - A Dark Alley\n"

    # Create a RoomMap object
    parsed_room = RoomMap(LOOK_OUTPUT, EXITS_OUTPUT)
    print(parsed_room)
    print(json.dumps(parsed_room.to_dict(), indent=4))

    # Connect another room to the north exit
    parsed_room.map_room_to_exit(
        "N", RoomMap("Another room", "Obvious exits:\nSouth - Tavern\n")
    )

    # Display updated room info
    print(parsed_room)
    print(json.dumps(parsed_room.to_dict(), indent=4))
