# $${\color{lightblue}MiA\ -\ AI\ Assistant\ for\ Linux}$$

**MiA** is an AI-powered assistant designed to help you control your **Linux** machine using natural language commands.
By utilizing the **free ChatGPT** API, MiA transforms user prompts into Linux commands to interact with the system. 
It's fully customizable and features **multi-theme support**, **chat history tracking** and **root password handling**.
MiA is a powerful tool that makes interacting with your machine more intuitive.

<br>

# $${\color{lightgreen}Features}$$

+ **AI-Powered Control**: Uses the ChatGPT API to process and turn natural language commands into Linux commands.
+ **Multi-Theme Support**: Choose from various themes to personalize the assistant's appearance and interface.
+ **Customizable via .env File**: Configure themes, API keys, and other settings directly from the .env file.
+ **Chat History**: MiA stores your conversation history for reference and better context handling.
+ **Root Password Support**: Prompts for the root password securely when necessary, allowing MiA to perform administrative tasks.

> [!WARNING]
> **No Terminal Execution for root**: MiA cannot be run directly from the terminal due to password prompting (only for root commands). You need to create launchers or use a graphical interface to run it.

<br>

# $${\color{lightblue}Requirements}$$

+ Linux-based operating system
+ Python 3.x
+ Dependencies inside `requirements.txt`
+ Internet connection for API access

<br>

# $${\color{yellow}Installation}$$

1. Clone the Repository:
  ```bsah
  git clone https://github.com/yourusername/MiA.git
  cd MiA
  ```
2. Set Up Virtual Environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
3. Install Dependencies:
  ```bash
  pip install -r requirements.txt
  ```
4. Configure the `.env` for global settings:<br>
   - Change system message if you need to customize your prompt preferences
   - Change api endpoint url and header if you want to use your own api

5. run the app using **Flet** or **Python**:
> [!NOTE]
> Since MiA requires root access for some commands, do not run it directly from the terminal. Instead, create a launcher or use your system's GUI to launch it. (I will fix that later)

```bash
flet tun mia.py
pytion mia.py
```

<br>

# $${\color{blue}Usage}$$
Once the setup is complete, you can launch MiA using a launcher or through the graphical user interface (GUI).
You will be prompted for your root password when necessary. 
The assistant will then process your commands and execute them on your system.
## Example command:
* **User**: "Install Python 3"
* **MiA**: Translates the request into a Linux command (sudo apt install python3) and prompts for the root password

<br>

# $${\color{red}Limitations}$$
+ **Terminal Restrictions**: MiA cannot be run directly from the terminal due to the root password prompt (for no-root comments, it's OK). Always use a launcher or graphical tool.
+ **Limited Commands**: While MiA can handle most common Linux tasks, it may not support highly specific or custom commands in certain configurations.

<br>

# $${\color{lightblue}Upcoming\ Updates}$$
Stay tuned for upcoming features and improvements:
+ Enhanced root password handling
+ More customizable themes
+ Additional command support
+ Bug fixes and performance optimizations


<br>

# $${\color{green}Thank\ you\ for\ supporting\ this\ project}$$
Hope you like it :D
