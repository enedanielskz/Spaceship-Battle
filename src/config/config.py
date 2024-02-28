import configparser

# Get the configurations from the "config.ini" file
config = configparser.ConfigParser()
config.read("config.ini")

"""
# WINDOW PROPERTIES
config.getint("WINDOW_PROPERTIES", "width")
config.getint("WINDOW_PROPERTIES", "height")
config.getboolean("WINDOW_PROPERTIES", "fullscreen")
config.getint("WINDOW_PROPERTIES", "fps")
config.getboolean("WINDOW_PROPERTIES", "show_fps")


# PLAYERS STATS
config.getint("PLAYERS_STATS", "health")
config.getint("PLAYERS_STATS", "lasers")


# PLAYER1 CONTROLS
get_key(config.get("PLAYER1_CONTROLS", "left"))
get_key(config.get("PLAYER1_CONTROLS", "right"))
get_key(config.get("PLAYER1_CONTROLS", "up"))
get_key(config.get("PLAYER1_CONTROLS", "down"))
get_key(config.get("PLAYER1_CONTROLS", "fire"))


# PLAYER2 CONTROLS
get_key(config.get("PLAYER2_CONTROLS", "left"))
get_key(config.get("PLAYER2_CONTROLS", "right"))
get_key(config.get("PLAYER2_CONTROLS", "up"))
get_key(config.get("PLAYER2_CONTROLS", "down"))
get_key(config.get("PLAYER2_CONTROLS", "fire"))


# PLAYER1 COLOR
config.getint("PLAYER1_COLOR", "red")
config.getint("PLAYER1_COLOR", "green")
config.getint("PLAYER1_COLOR", "blue")


# PLAYER2 COLOR
config.getint("PLAYER2_COLOR", "red")
config.getint("PLAYER2_COLOR", "green")
config.getint("PLAYER2_COLOR", "blue")


# OTHER KEYS
get_key(config.get("OTHER_KEYS", "restart"))


# SOUND
config.getfloat("SOUND", "music")
config.getfloat("SOUND", "game")
config.getfloat("SOUND", "menu")


# EFFECTS
config.getboolean("EFFECTS", "glow")
"""


def save_config():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
