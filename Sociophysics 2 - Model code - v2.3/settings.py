# Units are the unit of the number you are changing. Example: 5 * pmc has a unit of m

### PREFORMANCE  SETTINGS ###
FRAME_RATE = 0                                              # Limits the display rate to a specified amount of frames per second, <= 0 does not limit the rate
STEPS_PER_SECOND = 60                                       # [1/s] Sets the amount of steps inside one second of moddeling time 
STEP_SIZE = 1/STEPS_PER_SECOND                              # [s]

### NUDGE SETTINGS ###
NUDGE_BONUS_BENCH = False
NUDGE_MOVE_PATH = False
NUDGE_DANGER_AWARENESS = False

### GENERAL SIZE SETTINGS ###
pmc = 18.5                                                  # [pixels/m] Pixels to Meters Conversion
TARGET_RADIUS = 0.75 * pmc                                  # [m] 

### SPAWNING ###
MAX_AGENTS = 70
SPAWN_TIME = 3                                           # [s] sets the amount of time on average between spawns
SPAWN_ATTEMPTS = 5                                          # Sets the amount of times agents are attempted to spawn per tick
SPAWN_PROBABILITY = STEP_SIZE/(SPAWN_ATTEMPTS * SPAWN_TIME) # Sets the probability of an agent spawning on a spawn attempt

### AGENT SETTINGS ###
AGENT_MASS = 70                                             # [Kg]
AGENT_SIGHT_ANGLE = 60                                      # [Degrees]
AGENT_SIGHT_UNIFORM_ANGLE = 2                               # [Degrees]
AGENT_SIGHT_DISTANCE = 20 * pmc                             # [m] Used in get sight value
AGENT_SIGHT_UNIFORM_DISTANCE = 8 * pmc                      # [m]  
AGENT_FORGET_TIME = 5                                       # [s]
AGENT_VELOCITY_BOUNDRY = 0.5 * pmc                         # [s] Determines if an agent is stationary or moving for agent vision.

START_VELOCITY_X = 0 * pmc                                  # [m/s] sets agents start velocity in the x direction
START_VELOCITY_Y = 0 * pmc                                  # [m/s] sets agents start velocity in the y direction

dangerzone_awareness = 0.7                                    # [Chance] Set the chance an agent is aware of the danger zone
WAIT_CHANCE = 0.12                                          # [Chance] 

### FORCE SETTINGS ###
TARGET_FORCE_SCALER = 250                                    # [Multiplier] [N]
REPULSION_FORCE_SCALAR = 270                                # [Multiplier]
REPULSION_DANGER_ZONE_SCALAR = 230                          # [Multiplier]
WALL_FORCE_SCALAR = 245                                     # [Multiplier]
FRICTION_FORCE_SCALAR = 6.9                                 # [Multiplier]
dangerzone_awerness_false_multiplier = 0.7                  # [Multiplier] Multiplies the dangerzone force a person who IS NOT aware of the dangerzone feels by this amount (compared to aware people)

DISTANCE_THRESHOLD = 5 * pmc                                # [m] The distance a force can act over
MIN_VELOCITY_FOR_FRICTION = 0.2 * pmc                       # [m/s]

WALL_CORNER_FORCE = True
USE_AGENT_AWARENESS_FOR_FORCE = True

### TARGET SELECTION SETTINGS ###
NUMBER_OF_POTENTIAL_TARGETS = 50                            # [-]
NEXT_TARGET_RANGE = 7 * pmc                                 # [m] Needs to be at least larger than TARGET_REACHED_RADIUS
TARGET_REACHED_RADIUS = 1.5 * pmc                           # [m] Sets the radius of the target in which the target is considerd reached
WAIT_CHANCE_MULTIPLIER = 0.8

TARGET_SPOT_BASE_WEIGHT = 0.001                             # [-] This value comes down to the chance that someone turns around.
TARGET_SPOT_WALL_WEIGHT = 0.0000001                         # [-]
TARGET_IN_SIGHT_MULTIPLIER = 2                            # [Multiplier]
BENCH_MULTIPLIER = 5                                       # [Multiplier]
CROWD_AVOIDANCE = 0.5                                       # [Multiplier] 
FORWARDS_MULTIPLIER = 100                                   # [Multiplier]
dangerzone_target_multiplier_aware = 0                      # [Multiplier]
dangerzone_target_multiplier_unaware = 1                    # [Multiplier]

SWITCH_TARGET_CHANCE = 0.001                                # [Chance]
SWITCH_TARGET_LOW_VELOCITY = 0                              # [Chance]
VELOCITY_TARGET_SWITCH = 0.5 * pmc                          # [m/s]

USE_AGENT_AWARENESS_FOR_TARGET = True

### DISPLAY SETTINGS ###
AGENT_RADIUS = 0.3 * pmc                                    # [m]
DISPLAY_WALLS = True
DISPLAY_LEGEND = True
DISPLAY_CONTROL = True
DISPLAY_TARGET = True
DISPLAY_CLOCK = True
DISPLAY_OVERSTEPPED_SECONDS = True
DISPLAY_TARGET_SELCTION = True
DISPLAY_ADVANCED_SPOT_COLORS = True                         # Displays the spot with a colormapping value for the weight ranging from 0 to 1.
DISPLAY_ADVANCED_SPOT_WEIGHT = True      
DISPLAY_PERFORMANCE_TIME = False
HEATMAP_STEPS = 32                                          # [-]
    
AGENT_DATA = False                                          # Prints data from agent class GIVES DATA IN METRIC UNITS
FORCE_DATA = True                                           # Prints data from force class GIVES DATA IN METRIC UNITS
AGENT_NUMBER_DATA = True                                   # Prints amount of agents on screen

### OTHER SETTINGS ###
WAIT_FROM = 13 * pmc                                        # [m] Agents start waiting from x pixels from the left
WAIT_INFLUENCE_RANGE = 3.5 * pmc
PLATFORM_DISTIBUTION_MEASUREMENT = True