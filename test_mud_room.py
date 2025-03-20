"""Unit tests for the mud_room module."""

import unittest
import hashlib
import uuid
from mud_room import Room


class TestRoom(unittest.TestCase):
    """
    Unit tests for the Room class.

    Tests the initialization, ID generation, exit mapping, dictionary conversion,
    and string representation of the Room class.
    """

    def setUp(self):
        """
        Set up test data before each test case.
        """
        self.look_output = "You are in a large hall with marble pillars."
        self.exits_output = "Obvious exits:\nNorth - Grand Corridor\nWest - Kitchen\n"
        self.room = Room(self.look_output, self.exits_output)

    def test_initialization(self):
        """
        Test that the Room object is initialized correctly with valid outputs.
        """
        expected_exits = {
            "N": "Grand Corridor",
            "W": "Kitchen",
        }
        self.assertEqual(self.room.raw_look_output, self.look_output)
        self.assertEqual(self.room.raw_exits_output, self.exits_output)
        self.assertEqual(self.room.exits, expected_exits)

    def test_generate_id_normal_case(self):
        """
        Test that the Room ID is correctly generated using an MD5 hash
        of the feature's string representation in normal cases.
        """
        expected_id = "92fd310cf71a43d58b55c6069bb071ab" 
        self.assertEqual(self.room.id, expected_id)

    def test_generate_id_pitch_black(self):
        """
        Test that the Room ID is correctly generated for the 'pitch black' scenario.
        The ID should start with 'black_' followed by a UUID.
        """
        room = Room("It is pitch black...", self.exits_output)
        self.assertTrue(room.id.startswith("black_"))
        self.assertTrue(uuid.UUID(room.id.split("_")[1]))



    def test_to_dict(self):
        """
        Test that the Room object is correctly converted to a dictionary format.
        """

        expected_dict = {
            "id": "92fd310cf71a43d58b55c6069bb071ab",
            "features": self.room.features.to_dict(),
            "raw_look_output": self.look_output,
            "raw_exits_output": self.exits_output,
            "exits": {
                "N": "Grand Corridor",
                "W": "Kitchen",
            },
        }

        self.assertEqual(self.room.to_dict(), expected_dict)

    def test_str(self):
        """
        Test that the string representation of the Room object is correctly formatted.
        """
        expected_str = (
            f"Features:\n{self.room.features}\n\n"
            "Exits:\nN: Grand Corridor\nW: Kitchen"
        )

        self.assertEqual(str(self.room), expected_str)


if __name__ == "__main__":
    unittest.main()
