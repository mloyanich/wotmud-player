"""
A module for testing the RoomFeatures class.

This module contains unit tests for the RoomFeatures class, which is responsible for parsing
and organizing text with ANSI color codes. The tests ensure that the class correctly extracts
and categorizes text segments based on their associated color codes.

Example usage:
    python -m unittest test_room_features.py
"""

import unittest
from mud_room_features import RoomFeatures


class TestRoomFeatures(unittest.TestCase):
    """
    A test case class for testing the RoomFeatures class.

    This class contains methods to test the functionality of the RoomFeatures class,
    including parsing input strings, extracting text segments by color, and mapping
    color codes to human-readable names.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method initializes an input string with ANSI color codes and creates an
        instance of the RoomFeatures class for testing.
        """
        self.input_string = (
            "\u001b[36mCrown and Lion Tavern\u001b[0m\r\n"
            "This noisy tavern seems a bustle of activity, day or night. There are rooms\n\r"
            "to rent upstairs, but they all seem to be full tonight. A chubby innkeeper\n\r"
            "and a slew of bar maids scurry about trying to keep up with the orders of\n\r"
            "the patrons. There is one open table stuck in the corner where you might be\n\r"
            "able to sip a quick drink. A small sign hangs from the wall.\n\r"
            "[ obvious exits: W ]\r\n"
            "\u001b[32m\u001b[33mA stout looking guard is here, walking the streets of Camelot.\n\r"
            "A ragged looking man asks for spare coins.\n\r"
            "A bartender serves customers with a greedy smile.\n\r"
            "A middle-aged woman offers drinks to patrons.\n\r"
            "A merchant guard eyes you warily, intent on keeping order.\r\n"
            "A merchant guard eyes you warily, intent on keeping order.\r\n"
            "A historian stands here, rattling on about some historical fact or other.\r\n"
            "\u001b[0m\r\n"
            "* HP:Healthy SP:Bursting MV:Fresh > "
        )
        self.room_features = RoomFeatures(self.input_string)

    def test_cyan_features(self):
        """
        Test the extraction of text segments with the cyan color code.

        This test verifies that the RoomFeatures class correctly extracts text segments
        associated with the cyan color code.
        """
        cyan_features = self.room_features.get_features_by_color(
            RoomFeatures.COLOR_CYAN
        )
        self.assertEqual(cyan_features, ["Crown and Lion Tavern"])

    def test_default_features(self):
        """
        Test the extraction of text segments with the default color code.

        This test verifies that the RoomFeatures class correctly extracts text segments
        associated with the default color code.
        """
        default_features = self.room_features.get_features_by_color(
            RoomFeatures.COLOR_DEFAULT
        )
        expected_default_features = [(
                "This noisy tavern seems a bustle of activity, day or night. "
                "There are rooms to rent upstairs, "
                "but they all seem to be full tonight. "
                "A chubby innkeeper and a slew of bar maids scurry about trying to keep "
                "up with the orders of the patrons. "
                "There is one open table stuck in the corner where you might be able to sip "
                "a quick drink. A small sign hangs from the wall."
            )]
           
        self.assertEqual(default_features, expected_default_features)

    def test_yellow_features(self):
        """
        Test the extraction of text segments with the yellow color code.

        This test verifies that the RoomFeatures class correctly extracts text segments
        associated with the yellow color code.
        """
        yellow_features = self.room_features.get_features_by_color(
            RoomFeatures.COLOR_YELLOW
        )
        expected_yellow_features = [
            "A stout looking guard is here, walking the streets of Camelot.",
            "A ragged looking man asks for spare coins.",
            "A bartender serves customers with a greedy smile.",
            "A middle-aged woman offers drinks to patrons.",
            "A merchant guard eyes you warily, intent on keeping order.",
            "A merchant guard eyes you warily, intent on keeping order.",
            "A historian stands here, rattling on about some historical fact or other.",
        ]
        self.assertCountEqual(yellow_features, expected_yellow_features)

    def test_green_features(self):
        """
        Test the extraction of text segments with the green color code.

        This test verifies that the RoomFeatures class correctly extracts text segments
        associated with the green color code.
        """
        green_features = self.room_features.get_features_by_color(
            RoomFeatures.COLOR_GREEN
        )
        self.assertEqual(green_features, [])

    def test_features_with_color_names(self):
        """
        Test the mapping of color codes to human-readable names.

        This test verifies that the RoomFeatures class correctly maps color codes to
        human-readable names and organizes the text segments accordingly.
        """
        features_with_names = self.room_features.to_dict()
        expected_features_with_names = {
            "name": "Crown and Lion Tavern",
            "items":[],
            "description": (
                    "This noisy tavern seems a bustle of activity, day or night. "
                    "There are rooms to rent upstairs, but they all seem to be full tonight. "
                    "A chubby innkeeper and a slew of bar maids scurry about trying to keep up "
                    "with the orders of the patrons. There is one open table stuck "
                    "in the corner where you might be able to sip a quick drink. "
                    "A small sign hangs from the wall."
                ),
            "mobs": [
                "A stout looking guard is here, walking the streets of Camelot.",
                "A ragged looking man asks for spare coins.",
                "A bartender serves customers with a greedy smile.",
                "A middle-aged woman offers drinks to patrons.",
                "A merchant guard eyes you warily, intent on keeping order.",
                "A merchant guard eyes you warily, intent on keeping order.",
                "A historian stands here, rattling on about some historical fact or other.",
            ],
            "raw": self.input_string,
        }
        self.assertEqual(features_with_names, expected_features_with_names)


if __name__ == "__main__":
    unittest.main()
