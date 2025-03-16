# mud_client.py

import asyncio
import telnetlib3
import logging
from config import HOST, PORT, USERNAME, PASSPHRASE  # Import from config.py


class MUDClient:
    def __init__(self, log_level=logging.INFO):
        """Initialize the MUD client with logging level."""
        # Configure logging
        self.logger = logging.getLogger("MUDClient")
        self.logger.setLevel(log_level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.reader = None
        self.writer = None

    async def connect(self):
        """Establish a connection to the MUD server."""
        self.reader, self.writer = await telnetlib3.open_connection(HOST, PORT)
        self.logger.info("Connected to %s:%d", HOST, PORT)  # Lazy formatting

    async def login(self):
        """Login to the MUD server using the provided credentials."""
        if not self.reader or not self.writer:
            raise Exception("Not connected to the server. Call connect() first.")

        # Wait for the custom prompt and send username
        output = await self.reader.readuntil(b"By what name do you wish to be known?")
        self.logger.debug(
            "Raw output before username prompt: %r", output
        )  # Lazy formatting
        self.writer.write(f"{USERNAME}\r\n")
        self.logger.debug("Sent username: %s", USERNAME)  # Lazy formatting

        # Wait for the passphrase prompt and send passphrase
        output = await self.reader.readuntil(b"Passphrase: ")
        self.logger.debug(
            "Raw output before passphrase prompt: %r", output
        )  # Lazy formatting
        self.writer.write(f"{PASSPHRASE}\r\n")
        self.logger.debug("Sent passphrase: %s", PASSPHRASE)  # Lazy formatting

        # Read the response after login
        output = await self.send_and_read(
            ""
        )  # Send an empty command to read the response
        self.logger.debug("Login response: %s", output)  # Lazy formatting

    async def send_and_read(self, command, timeout=2):
        """Send a command to the MUD server and read the output."""
        if not self.reader or not self.writer:
            raise Exception("Not connected to the server. Call connect() first.")

        # Send the command
        self.writer.write(f"{command}\r\n")
        self.logger.debug("Sent command: %s", command)  # Lazy formatting

        # Read the output
        output = ""
        try:
            while True:
                # Read data from the server
                chunk = await asyncio.wait_for(self.reader.read(1024), timeout)
                if not chunk:
                    break
                output += chunk
                self.logger.debug("Raw chunk received: %r", chunk)  # Lazy formatting
        except asyncio.TimeoutError:
            # Timeout reached, return what was read so far
            self.logger.debug(
                "Timeout reached while reading output."
            )  # Lazy formatting
        except ConnectionResetError:
            self.logger.error("Connection was reset by the server.")  # Lazy formatting
            output = ""
        except Exception as e:
            self.logger.error(
                "An error occurred while reading output: %s", e
            )  # Lazy formatting
            output = ""
        return output

    async def close(self):
        """Close the connection to the MUD server."""
        if self.writer:
            self.writer.close()  # Close the connection
            self.logger.info("Connection closed.")  # Lazy formatting
