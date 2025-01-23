#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Modules
import os
import json
import logging
import webbrowser
from typing import NoReturn, List, Dict

# Related 3rd-Party Modules
import flet as ft
from dotenv import load_dotenv

# Local Modules
from core import ai_process
from utils import get_last_command, run_command_with_sudo

# Load environment and Initialize logging
load_dotenv()
logging.basicConfig(level=logging.INFO)


def main(page: ft.Page) -> NoReturn:
    """
    Main Flet app function.

    Configures the application page, including theme, layout, and event handling. 
    Handles user interactions, such as processing commands, toggling themes, and
    managing UI elements like the bottom sheet for password prompts.
    """

    # ---------- Page Configuration ----------

    # Placement of the application
    if int(os.getenv("WINDOW_CENTER")):
        page.window.center()
    else:
        page.window.left = os.getenv("WINDOW_LEFT")
        page.window.top = os.getenv("WINDOW_TOP")

    page.title = os.getenv("TITLE")
    page.theme_mode = os.getenv("THEME")
    page.window.width = os.getenv("WINDOW_WIDTH")
    page.window.height = os.getenv("WINDOW_HEIGHT")

    page.padding = 0
    page.margin = 0
    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True

    # Font configurations
    if not os.path.isfile(f"{os.getenv("ASSETS_FOLDER")}/fonts/0xProto-Regular.ttf"):
        logging.warning("Custom font file not found. Using default font.")

    page.fonts = {
        "0xProto": "/fonts/0xProto-Regular.ttf"
    }

    # Color mapping
    color_palette: Dict[str, Dict[str, str]] = {
        "DARK": {
            "bg_color": "#181A21",
            "color_scheme_seed": "#239cd3",
            "secondary_bg_color": "#1c202b"
        },
        "LIGHT": {
            "bg_color": "#e4e4e4",
            "color_scheme_seed": "#0d4072",
            "secondary_bg_color": "#d6d6d6"
        }
    }

    # Theme configurations
    page.bgcolor = color_palette[page.theme_mode]["bg_color"]
    page.theme = ft.Theme(
        color_scheme_seed=color_palette[page.theme_mode]["color_scheme_seed"],
        font_family="0xProto"
    )    

    # Helper function to process user input
    def process(text_input: ft.TextField, 
                text_area: ft.ListView, 
                progress_bar: ft.ProgressBar) -> NoReturn:
        """
        Processes user input, updates the message log, and appends AI responses.

        Args:
            text_input (ft.TextField): The input field for user text.
            text_area (ft.ListView): The list view to display chat messages.
            progress_bar (ft.ProgressBar): Progress bar to show ongoing tasks.

        Returns:
            No Return
        """

        # Start progress bar
        progress_bar.value = None
        progress_bar.update()

        # Read messages
        with open("messages.json") as data:
            messages: List[Dict[str, str]] = json.load(data)

        # Add new prompt
        messages.append({
            "role": "user",
            "content": text_input.value.strip()
        })

        # Process input
        result: str = ai_process(messages)

        # Check if the command contains `sudo` and prompt for password
        if "sudo" in result:
            # Retrieve last command from the file
            last_command: str = get_last_command()
            show_password_prompt(
                command=last_command,
                text_area=text_area, 
                progress_bar=progress_bar
            )
        
        else:
            # Show result
            text_area.controls.append(
                ft.Text(result, selectable=True)
            )
            text_area.update()

        # Stop progress bar
        progress_bar.value = 0
        progress_bar.update()


    # Show a bottom sheet for password input
    def show_password_prompt(command: str, 
                             text_area: ft.ListView, 
                             progress_bar: ft.ProgressBar) -> NoReturn:
        """
        Prompts password to user, to get root password and re-runs the 
        command

        Args:
            command (str): the command to run.
            text_area (ft.ListView): The list view to display chat messages.
            progress_bar (ft.ProgressBar): Progress bar to show ongoing tasks.

        Returns:
            No Return
        """
        
        # Handle password submission and execute the command
        def on_submit_password(event):
            password: str = password_input.value
            if password:
                # Run the command with the entered password
                output: str = run_command_with_sudo(
                    command=command,
                    password=password
                )
                text_area.controls.append(
                    ft.Text(value=output, selectable=True)
                )
                text_area.update()

            # Hide the bottom sheet after processing
            bottom_sheet.open = False
            page.update()
        
        # Update bottom sheet content dynamically
        password_input: ft.TextField = ft.TextField(
            label="Sudo password required",
            password=True,
            dense=True,
            hint_text="Enter your password...",
            hint_style=ft.TextStyle(color="#555555"),
            on_submit=on_submit_password
        )

        # Add container to bottom sheet
        bottom_sheet.content = ft.Container(
            content=ft.Column(
                controls=[
                    password_input,
                    ft.TextButton(
                        text="Submit", 
                        on_click=on_submit_password
                    )
                ],
                tight=True
            ),
            bgcolor=color_palette[page.theme_mode]["bg_color"],
            padding=5,
        )

        # Display the bottom sheet
        bottom_sheet.open = True
        page.update()


    # Clear the cat history
    def clear_chat(text_area: ft.ListView) -> NoReturn:
        text_area.controls = []
        text_area.update()

    # Open repository in GitHub
    def open_github() -> NoReturn:
        webbrowser.open("https://github.com/Kourva/MiA")

    # Change color palette
    def change_palette(popup_menu, bottom_sheet, icon) -> NoReturn:
        page.theme_mode = "DARK" if page.theme_mode == "LIGHT" else "LIGHT"
        page.bgcolor = color_palette[page.theme_mode]["bg_color"]
        popup_menu.bgcolor = color_palette[page.theme_mode]["secondary_bg_color"]
        bottom_sheet.content.bgcolor = color_palette[page.theme_mode]["bg_color"]
        icon.color = color_palette["DARK" if page.theme_mode == "LIGHT" else "LIGHT"]["bg_color"]
        page.update()

    # ---------- UI Components ----------
    # Progress bar
    progress_bar: ft.ProgressBar = ft.ProgressBar(
        value=0, 
        bgcolor=ft.Colors.TRANSPARENT
    )

    # Command output area
    text_area: ft.ListView = ft.ListView(
        expand=1, 
        spacing=10, 
        padding=20, 
        auto_scroll=True, 
        controls=[
            ft.Text(value="What can i do for you?", selectable=True)
        ]
    )

    # Text input
    text_input: ft.TextField = ft.TextField(
        adaptive=True,
        label="$ Message",
        dense=True,
        multiline=True,
        max_lines=2,
        border_radius=0,
        shift_enter=True,
        hint_text="\\n -> SHift+ENTER.",
        hint_style=ft.TextStyle(color="#555555"),
        on_submit=lambda _: process(
            text_input=text_input, 
            text_area=text_area, 
            progress_bar=progress_bar
        )
    )

    # Password input
    password_input = ft.TextField(
        label="Sudo password required",
        password=True,
        dense=True,
        hint_text="Enter your password...",
        hint_style=ft.TextStyle(color="#555555")
    )

    # Bottom sheet
    bottom_sheet: ft.BottomSheet = ft.BottomSheet(
        open=False,
        enable_drag=False,
        content=ft.Container()
    )

    # Add components to page
    page.add(
        ft.Row(
            spacing=0,
            controls=[
                ft.WindowDragArea(
                    ft.Container(
                        ft.Row(
                            controls=[
                                icon := ft.Image(
                                    src=f"/icons/icon.png",
                                    width=25,
                                    height=25,
                                    fit=ft.ImageFit.CONTAIN,
                                    color=color_palette["DARK" if page.theme_mode == "LIGHT" else "LIGHT"]["bg_color"]
                                ),
                                ft.Text(
                                    value=os.getenv("TITLE"),
                                    weight="bold",
                                    color="#239cd3",
                                    size=22
                                )
                            ]
                        ),
                        bgcolor=ft.Colors.TRANSPARENT,
                        padding=10
                    ),
                    expand=True
                ),
                popup_menu := ft.PopupMenuButton(
                    bgcolor=color_palette[page.theme_mode]["secondary_bg_color"],
                    shape=ft.BeveledRectangleBorder(radius=5),
                    menu_position=ft.PopupMenuPosition.UNDER,
                    items=[
                        ft.PopupMenuItem(
                            text="Switch Theme",
                            icon="palette",
                            height=30,
                            on_click=lambda _: change_palette(
                                popup_menu=popup_menu, 
                                bottom_sheet=bottom_sheet, 
                                icon=icon
                            )
                        ),
                        ft.PopupMenuItem(
                            text="Clear Chat",
                            icon="clear",
                            height=30,
                            on_click=lambda _: clear_chat(text_area)
                        ),
                        ft.PopupMenuItem(
                            text="Github",
                            icon="public",
                            height=30,
                            on_click=lambda _: open_github()
                        ),
                    ]
                ),
                ft.IconButton(
                    "close",
                    on_click=lambda _: page.window.close()
                )
            ]
        ),
        progress_bar,
        text_area,
        ft.Container(content=text_input, padding=5),
        bottom_sheet
    )

# Run the flet app
if __name__ == "__main__":
    ft.app(
        main, 
        assets_dir=os.getenv("ASSETS_FOLDER")
    )