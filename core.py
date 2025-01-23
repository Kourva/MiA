#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Modules
import os
import shlex
import json
import logging
import subprocess
from typing import List, Dict

# Related Third-Party Modules
import requests
from dotenv import load_dotenv

# Local Modules
from utils import save_last_command, update_messages

# Load environment and Initialize logging
load_dotenv()
logging.basicConfig(level=logging.INFO)

def ai_process(messages: List[Dict[str, str]]) -> str:
    """
    Chat completion for Remix AI. Converts a list of messages into a command 
    and executes it using a Python subprocess.

    Parameters:
        messages (List[Dict[str, str]]): Conversation history.

    Returns:
        result str: The result of the executed command.
    """
    url: str = os.getenv("REQUEST_URL")
    headers: Dict[str, str] = json.loads(os.getenv("REQUEST_HEADERS"))
    data = {"prompt": str(messages)}

    try:
        # Request to the AI endpoint
        response: requests.Response = requests.post(
            url=url, 
            json=data, 
            headers=headers
        )
        response.raise_for_status()
        response_data = response.json()

        if 'choices' in response_data and response_data['choices']:
            command: str = response_data['choices'][0]['message']['content'].strip()

            # Save the command to the file
            save_last_command(command)
            update_messages(message=command, role="assistant")

            # Check and run the command
            return check_command_permission(command)
        else:
            return f"Unexpected response format: {response_data}"

    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except (KeyError, ValueError) as e:
        return f"Error processing response: {e}"

def check_command_permission(command: str) -> str:
    """
    Checks if a command requires sudo and runs it with or without sudo.

    Parameters:
        command (str): Command to execute.

    Returns:
        str: Command output.
    """
    # If the command already has sudo, run it directly
    if command.startswith("sudo"):
        return run_command(command)

    # Run command without sudo first
    result: str = run_command(command)

    # Retry with sudo if needed
    if "Permission denied" in result:
        logging.warning("Permission denied. Retrying with sudo...")
        return run_command(f"sudo {command}")

    return result


def run_command(command: str) -> str:
    """
    Runs a shell command, optionally using sudo.

    Parameters:
        command (str): The command to execute.

    Returns:
        str: Command output .
    """
    try:
        # Use shlex.split for safer command splitting
        command_parts: List[str] = shlex.split(command)

        result: subprocess.run = subprocess.run(
            command_parts,
            capture_output=True,
            text=True
        )

        # Return command output or error
        if result.returncode == 0:
            return f"Command executed successfully:\n{result.stdout}"
        else:
            return f"Command failed:\n{result.stderr}"

    except Exception as e:
        return f"Error while executing command: {e}"