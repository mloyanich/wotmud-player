import unittest
import uuid

from mud_room_map import RoomMap


class TestRoomMap(unittest.TestCase):
    """
    Unit tests for the RoomMap class.
    """

    def setUp(self):
        """
        Set up test cases with sample look and exits output.
        """
        self.look_output = "You are in a large hall with marble pillars."
        self.exits_output = "Obvious exits:\nNorth - Grand Corridor\nWest - Kitchen\n"
        self.room_map = RoomMap(self.look_output, self.exits_output)

    def test_initialization(self):
        """
        Test that the RoomMap object is initialized correctly.
        """
        expected_exits = {
            "N": "Grand Corridor",
            "W": "Kitchen",
        }

        self.assertEqual(self.room_map.raw_look_output, self.look_output)
        self.assertEqual(self.room_map.raw_exits_output, self.exits_output)
        self.assertEqual(self.room_map.exits, expected_exits)

    def test_generate_id_normal_case(self):
        """
        Test that the room ID is correctly generated from the room's features.
        """
        expected_id = "92fd310cf71a43d58b55c6069bb071ab"
        self.assertEqual(self.room_map.id, expected_id)

    def test_generate_id_pitch_black(self):
        """
        Test that a unique ID is generated when the room is pitch black.
        """
        room = RoomMap("It is pitch black...", self.exits_output)
        self.assertTrue(room.id.startswith("black_"))
        self.assertTrue(uuid.UUID(room.id.split("_")[1]))

    def test_map_room_to_exit_valid(self):
        """
        Test that a room can be correctly mapped to an exit.
        """
        connected_room = RoomMap("Another room", "Obvious exits:\nSouth - Hall\n")
        self.room_map.map_room_to_exit("N", connected_room.id)

        self.assertEqual(self.room_map.exits["N"], connected_room.id)

    def test_map_room_to_exit_invalid(self):
        """
        Test that an invalid exit direction raises a ValueError.
        """
        connected_room = RoomMap("Another room", "Obvious exits:\nSouth - Hall\n")

        with self.assertRaises(ValueError) as context:
            self.room_map.map_room_to_exit("X", connected_room)

        self.assertEqual(str(context.exception), "Invalid exit direction: X")

    def test_to_dict(self):
        """
        Test that the RoomMap to_dict method returns the correct structure.
        """
        connected_room = RoomMap("Another room", "Obvious exits:\nSouth - Hall\n")
        self.room_map.map_room_to_exit("N", connected_room.id)

        expected_dict = {self.room_map.id: {"N": connected_room.id, "W": "Kitchen"}}

        self.assertEqual(self.room_map.to_dict(), expected_dict)

    def test_to_dict_no_connections(self):
        """
        Test that to_dict works correctly when there are no connected rooms.
        """
        expected_dict = {self.room_map.id: {"N": "Grand Corridor", "W": "Kitchen"}}

        self.assertEqual(self.room_map.to_dict(), expected_dict)

    def test_str(self):
        """
        Test that the __str__ method returns the expected string format.
        """
        connected_room = RoomMap("Another room", "Obvious exits:\nSouth - Hall\n")
        self.room_map.map_room_to_exit("N", connected_room.id)

        expected_str = (
            f"ID: {self.room_map.id}\nExits:\nN: {connected_room.id}\nW: Kitchen"
        )

        self.assertEqual(str(self.room_map), expected_str)

    def test_str_no_connections(self):
        """
        Test that the __str__ method works correctly with no connected rooms.
        """
        expected_str = f"ID: {self.room_map.id}\nExits:\nN: Grand Corridor\nW: Kitchen"

        self.assertEqual(str(self.room_map), expected_str)


if __name__ == "__main__":
    unittest.main()
