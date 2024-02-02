import random

# Agent colors
AGENT_BASE_COLOR = (255, 150, 150, 0.5)
AGENT_IN_DANGER_COLOR = (255, 0, 0)
AGENT_KNOWN_COLOR = (0, 255, 0)
AGENT_KNOWN_IN_DANGER_COLOR = (200, 200, 0)
AGENT_SELECTED_COLOR = (0, 0, 255)
AGENT_SELECTED_IN_DANGER_COLOR = (200, 0, 200)
AGENT_TARGET_COLOR = (0, 200, 200)
AGENT_WAITING_COLOR = (250, 250, 250)

# Environment colors
BENCH_COLOR = (200, 150, 200)
WALL_COLOR = (100, 100, 100)
DANGER_ZONE_COLOR = (200, 60, 60)
SPAWNING_AREA_COLOR = (255, 128, 0)
MOVE_PATH_COLOR = (100, 200, 100)

# Display colors
TEXT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (100, 100, 100)
SHAPE_BASE_COLOR = (200, 200, 200)
BUTTON_BASE_COLOR = (120, 120, 120)
BUTTON_EDGE_COLOR = (90, 90, 90)
BUTTON_ACTIVE_COLOR = (170, 200, 170)
BUTTON_UNACTIVE_COLOR = (200, 170, 170)

# Target colors
SPOT_COLOR = (100, 200, 150)
SPOT_WEIGHT_COLOR = (255, 255, 255) # Used for diplay setting DISPLAY_ADVANCED_SPOT_WEIGHT

# Legend colors
LEGEND_BACKGROUND = (120, 120, 120)
LEGEND_EDGE = (90, 90, 90)
LEGEND_TEXT = (255, 255, 255)

def get_random_color() -> tuple:
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return (red, green, blue)

def get_button_color(active:bool) -> bool:
    if active:
        return BUTTON_ACTIVE_COLOR
    else:
        return BUTTON_UNACTIVE_COLOR

def get_agent_color(selected:bool, in_danger_zone:bool, known:bool, waiting:bool) -> tuple:
    if (waiting):
        return AGENT_WAITING_COLOR
    
    if (selected and in_danger_zone):
        return AGENT_SELECTED_IN_DANGER_COLOR
    elif (selected):
        return AGENT_SELECTED_COLOR
    elif (known and in_danger_zone):
        return AGENT_KNOWN_IN_DANGER_COLOR
    elif (known):
        return AGENT_KNOWN_COLOR
    elif (in_danger_zone):
        return AGENT_IN_DANGER_COLOR
    else:
        return AGENT_BASE_COLOR
