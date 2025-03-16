import re


def clean_text(text):
    # Remove ANSI escape codes using regex
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    cleaned_text = ansi_escape.sub("", text)

    # Replace \r\n and \n\r with \n for consistent line breaks
    cleaned_text = cleaned_text.replace("\r\n", "\n").replace("\n\r", "\n")

    # Remove trailing and leading whitespace
    cleaned_text = cleaned_text.strip()

    return cleaned_text
