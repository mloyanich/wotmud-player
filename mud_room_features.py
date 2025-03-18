"""
A module for parsing and organizing text with ANSI color codes into a structured format.

This module provides the `RoomFeatures` class, which is designed to process input strings
containing ANSI color codes and extract text segments based on their associated colors.
The parsed data is organized into a dictionary, allowing easy access to text segments
by their color codes or human-readable color names.

Example usage:
    raw_text = "\u001b[36mCrown and Lion Tavern\u001b[0m\r\n..."
    rf = RoomFeatures(raw_text)
    print(rf.get_features_by_color(RoomFeatures.COLOR_CYAN))
    print(rf.get_features_with_color_names())
"""

import re
import json
import logging
from constants import APPLICATION_NAME

module_logger = logging.getLogger(f"{APPLICATION_NAME}")


class RoomFeatures:
    """
    A class to parse and organize text with ANSI color codes.

    This class processes input strings containing ANSI color codes and extracts text
    segments based on their associated colors. The parsed data is stored in a dictionary
    for easy access.

    Attributes:
        COLOR_CYAN (str): ANSI color code for cyan.
        COLOR_GREEN (str): ANSI color code for green.
        COLOR_YELLOW (str): ANSI color code for yellow.
        COLOR_DEFAULT (str): ANSI color code for default (reset).
        input_string (str): The raw input string containing ANSI color codes and text.
        color_text_dict (dict): A dictionary mapping color codes to lists of text segments.
    """

    # Define color constants
    COLOR_CYAN = "\u001b[36m"
    COLOR_GREEN = "\u001b[32m"
    COLOR_YELLOW = "\u001b[33m"
    COLOR_DEFAULT = "\u001b[0m"

    def __init__(self, input_string):
        """
        Initializes a RoomFeatures object with the input string.

        Args:
            input_string (str): The raw input string containing ANSI color codes and text.
        """
        self.logger = logging.getLogger(
            f"{APPLICATION_NAME}.room_features.RoomFeatures"
        )
        self.input_string = input_string
        self.color_text_dict = self._parse_input_string()

    def _parse_input_string(self):
        """
        Parses the input string to extract text segments and their associated color codes.

        This method uses a regular expression to identify ANSI color codes and the text
        they colorize. The results are organized into a dictionary where keys are color
        codes and values are lists of text segments.

        Returns:
            dict: A dictionary mapping color codes to lists of text segments.
        """
        # Regular expression to match ANSI color codes and the text they colorize
        ansi_regex = re.compile(r"(\u001b\[\d+m)([^\u001b]*)")

        # Find all matches
        matches = ansi_regex.findall(self.input_string)

        # Organize the matches into a dictionary
        color_text_dict = {}
        current_color = self.COLOR_DEFAULT  # Start with the default color

        for match in matches:
            self.logger.debug("Processing match: %s", match)  # Debug: Print the match
            color_code, text = match

            # If a color code is found, update the current color
            if color_code:
                # Handle combined color codes (e.g., \u001b[32m\u001b[33m)
                for code in re.findall(r"\u001b\[\d+m", color_code):
                    if code == self.COLOR_GREEN:
                        current_color = self.COLOR_GREEN
                    elif code == self.COLOR_YELLOW:
                        current_color = self.COLOR_YELLOW
                    elif code == self.COLOR_CYAN:
                        current_color = self.COLOR_CYAN
                    else:
                        current_color = self.COLOR_DEFAULT  # Fallback to default

            # If no color code is found, assume default (white) color
            else:
                current_color = self.COLOR_DEFAULT

            # Skip empty text
            if not text.strip():
                continue

            # Handle default color logic
            if current_color == self.COLOR_DEFAULT:
                text = text.replace("\n\r", " ")
            text_segments = text.strip().replace("\r", "").split("\n")

            if current_color not in color_text_dict:
                color_text_dict[current_color] = []
            color_text_dict[current_color].extend(
                [segment for segment in text_segments if segment]
            )

        return color_text_dict

    def get_features_by_color(self, color_code):
        """
        Returns the text segments associated with a specific color code.

        Args:
            color_code (str): The ANSI color code to filter text segments by.

        Returns:
            list: A list of text segments associated with the specified color code.
        """
        return self.color_text_dict.get(color_code, [])

    def to_dict(self):
        """
        Returns the parsed features with human-readable color names.

        This method maps the internal color codes to human-readable names (e.g., "name",
        "items", "mobs", "description") and returns the parsed features in a more
        user-friendly format.

        Returns:
            dict: A dictionary mapping human-readable color names to lists of text segments.
        """
        color_name_map = {
            self.COLOR_CYAN: "name",
            self.COLOR_GREEN: "items",
            self.COLOR_YELLOW: "mobs",
            self.COLOR_DEFAULT: "description",
        }
        return {color_name_map.get(k, k): v for k, v in self.color_text_dict.items()}

    def __str__(self):
        """
        Returns a string representation of the parsed features.

        Returns:
            str: A string representation of the parsed features with human-readable color names.
        """
        features_with_color_names_str = "\n".join(
            [
                f"{color_name} : {'\n'.join(text_segments)}"
                for color_name, text_segments in self.to_dict().items()
            ]
        )
        return features_with_color_names_str


if __name__ == "__main__":
    RAW_TEXT = (
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

    # Print the raw input string to verify special characters
    module_logger.info("Raw Input String:")
    module_logger.info(repr(RAW_TEXT))  # Use repr() to show escape sequences

    rf = RoomFeatures(RAW_TEXT)

    module_logger.info("Parsed Features:")
    module_logger.info(rf)
    module_logger.info(json.dumps(rf.to_dict(), indent=4))
