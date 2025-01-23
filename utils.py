#!/usr/bin/env bash
# -*- coding: utf-8 -*-


# Standard Library Modules
import os
import json
import shlex
import logging
import subprocess
from typing import List, Dict, Union, NoReturn

# Related 3rd-Party modules
from dotenv import load_dotenv

# Load environment and Initialize logging
load_dotenv()
logging.basicConfig(level=logging.INFO)

# Get last command file path
LAST_COMMAND_FILE: str = os.getenv("LAST_COMMAND_FILE")


def save_last_command(command: str) -> NoReturn:
    """
    Save the last command to a file.

    Parameters:
        command (str): The command to save.
    """
    if not LAST_COMMAND_FILE:
        raise ValueError("Environment variable 'LAST_COMMAND_FILE' is not set.")

    if not os.path.isfile(LAST_COMMAND_FILE):
        raise FileNotFoundError(f"File '{LAST_COMMAND_FILE}' does not exist.")
        
    try:
        with open(LAST_COMMAND_FILE, "w") as file:
            file.write(command)
    except (OSError, IOError) as e:
        logging.error(f"Error saving last command: {e}")


def get_last_command() -> Union[str, None]:
    """
    Retrieve the last command from the file.

    Returns:
        Union[str, None]: The last saved command or None if not found.
    """
    if not LAST_COMMAND_FILE:
        raise ValueError("Environment variable 'LAST_COMMAND_FILE' is not set.")

    try:
        with open(LAST_COMMAND_FILE, "r") as file:
            return file.read().strip()
    except (OSError, IOError) as e:
        logging.error(f"Error reading last command: {e}")
        return None


def run_command_with_sudo(command: str, password: str) -> str:
    """
    Executes a command with sudo privileges using the provided password.

    Parameters:
        command (str): The command to run (without sudo).
        password (str): The sudo password.

    Returns:
        str: Command output or error message.
    """
    try:

        # Validate command
        if not command or not isinstance(command, str):
            return "Invalid command provided."

        # Split the command into parts, taking care of quotes
        try:
            command_parts: List[str] = shlex.split(command)
        except ValueError as e:
            return f"Error parsing command: {e}"

        # Ensuring command is valid (no `sudo` prefix expected)
        if command_parts[0].lower() == "sudo":
            command_parts = command_parts[1:]

        if not command_parts:
            return "Invalid command structure after removing `sudo`."


        # Execute command with sudo
        result = subprocess.run(
            ["sudo", "-S"] + command_parts,
            input=f"{password}\n",
            text=True,
            capture_output=True,
        )

        if result.returncode == 0:
            return f"Command executed successfully:\n{result.stdout}"
        else:
            return f"Command failed:\n{result.stderr}"

    except Exception as e:
        return f"Error executing command: {e}"


def update_messages(message: str, role: str) -> NoReturn:
    """
    Updates the messages (conversation history)

    Parameters:
        message (str): The message to add to history.
        role (str): The role of message

    Returns:
        no return
    """
    try:
        # Check if the file exists; create if not
        if not os.path.isfile("messages.json"):
            logging.warning("File 'messages.json' not found. Creating a new one.")
            with open("messages.json", "w") as file:
                json.dump([{
                    "role": "system",
                    "content": os.getenv["SYSTEM_MESSAGE"]
                }], file, indent=4)

        # Read the messages from the file
        with open("messages.json", "r") as file:
            messages: List[Dict[str, str]] = json.load(file)

        # Append the new message
        messages.append({"role": role, "content": message})

        # Write updated messages back to the file
        with open("messages.json", "w") as file:
            json.dump(messages, file, indent=4, ensure_ascii=False)

    except (OSError, IOError, json.JSONDecodeError) as e:
        logging.error(f"Error updating 'messages.json': {e}")
        raise


