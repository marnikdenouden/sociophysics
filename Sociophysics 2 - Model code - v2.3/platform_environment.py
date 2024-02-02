import pygame
from environment import Environment, Wall, Bench, DangerZone, SpawningRectangle, Rail_wall, MovePath
from display import Display, Image

# Constants to use from the platform environment
WIDTH, HEIGHT = 1480, 300
DISPLAY_SIZE = (WIDTH, HEIGHT)
BACKGROUND = Image("images/platform.png", 0, 0)
PLATFORM = Environment("platform")
PLATFORM_NUDGE_BENCH = Environment("platform_nudge_bench")
PLATFORM_NUDGE_WALKING_PATH = Environment("platform_nudge_walking_path")
PLATFORM_NUDGE_BOTH = Environment("platform_nudge_both")
TOP_DANGERZONE = DangerZone(0, 0, WIDTH, 63)
BOTTOM_DANGERZONE = DangerZone(0, (HEIGHT - 25 - 16), WIDTH, 70)

def setup():
    if __name__ == '__main__':
        # Pygame setup
        pygame.init()

        display = Display("Testing platform environment", (WIDTH, HEIGHT))
        display.add(BACKGROUND)

        # Top wall
        PLATFORM.add(Rail_wall(0, 0, WIDTH, 47))
        PLATFORM_NUDGE_BENCH.add(Rail_wall(0, 0, WIDTH, 47))
        PLATFORM_NUDGE_WALKING_PATH.add(Rail_wall(0, 0, WIDTH, 47))
        PLATFORM_NUDGE_BOTH.add(Rail_wall(0, 0, WIDTH, 47))

        # Left wall
        PLATFORM.add(Wall(0, 0, 10, HEIGHT))
        PLATFORM_NUDGE_BENCH.add(Wall(0, 0, 10, HEIGHT))
        PLATFORM_NUDGE_WALKING_PATH.add(Wall(0, 0, 10, HEIGHT))
        PLATFORM_NUDGE_BOTH.add(Wall(0, 0, 10, HEIGHT))

        # Right wall
        PLATFORM.add(Wall((WIDTH - 15), 0, 15, HEIGHT))
        PLATFORM_NUDGE_BENCH.add(Wall((WIDTH - 15), 0, 15, HEIGHT))
        PLATFORM_NUDGE_WALKING_PATH.add(Wall((WIDTH - 15), 0, 15, HEIGHT))
        PLATFORM_NUDGE_BOTH.add(Wall((WIDTH - 15), 0, 15, HEIGHT))

        # Bottom wall
        PLATFORM.add(Rail_wall(0, (HEIGHT - 25), WIDTH, 250))
        PLATFORM_NUDGE_BENCH.add(Rail_wall(0, (HEIGHT - 25), WIDTH, 250))
        PLATFORM_NUDGE_WALKING_PATH.add(Rail_wall(0, (HEIGHT - 25), WIDTH, 250))
        PLATFORM_NUDGE_BOTH.add(Rail_wall(0, (HEIGHT - 25), WIDTH, 250))

        # Bottom stair wall
        PLATFORM.add(Wall(0, 220, 160, 20))
        PLATFORM_NUDGE_BENCH.add(Wall(0, 220, 160, 20))
        PLATFORM_NUDGE_WALKING_PATH.add(Wall(0, 220, 160, 20))
        PLATFORM_NUDGE_BOTH.add(Wall(0, 220, 160, 20))

        # Top stair wall
        PLATFORM.add(Wall(0, 85, 160, 20))
        PLATFORM_NUDGE_BENCH.add(Wall(0, 85, 160, 20))
        PLATFORM_NUDGE_WALKING_PATH.add(Wall(0, 85, 160, 20))
        PLATFORM_NUDGE_BOTH.add(Wall(0, 85, 160, 20))
        
        # Move path top
        PLATFORM_NUDGE_WALKING_PATH.add(MovePath(36.55/80 * WIDTH, 3/12.2 * HEIGHT, 16/80 * WIDTH, 0.8/12.2 * HEIGHT))
        PLATFORM_NUDGE_BOTH.add(MovePath(36.55/80 * WIDTH, 3/12.2 * HEIGHT, 16/80 * WIDTH, 0.8/12.2 * HEIGHT))

        # Move path bottom
        PLATFORM_NUDGE_WALKING_PATH.add(MovePath(36.55/80 * WIDTH, 9.2/12.2 * HEIGHT, 16/80 * WIDTH, 0.8/12.2 * HEIGHT))
        PLATFORM_NUDGE_BOTH.add(MovePath(36.55/80 * WIDTH, 9.2/12.2 * HEIGHT, 16/80 * WIDTH, 0.8/12.2 * HEIGHT))

        # Kiosk
        PLATFORM.add(Wall(33.8/80 * WIDTH, 5/12.2 * HEIGHT, 21.5/80 * WIDTH, 3/12.2 * HEIGHT))
        PLATFORM_NUDGE_BENCH.add(Wall(33.8/80 * WIDTH, 5/12.2 * HEIGHT, 21.5/80 * WIDTH, 3/12.2 * HEIGHT))
        PLATFORM_NUDGE_WALKING_PATH.add(Wall(33.8/80 * WIDTH, 5/12.2 * HEIGHT, 21.5/80 * WIDTH, 3/12.2 * HEIGHT))
        PLATFORM_NUDGE_BOTH.add(Wall(33.8/80 * WIDTH, 5/12.2 * HEIGHT, 21.5/80 * WIDTH, 3/12.2 * HEIGHT))

        # 2nd building
        PLATFORM.add(Wall(77.8/80*WIDTH, 5/12.2*HEIGHT, 500, 3/12.2*HEIGHT))
        PLATFORM_NUDGE_BENCH.add(Wall(77.8/80*WIDTH, 5/12.2*HEIGHT, 500, 3/12.2*HEIGHT))
        PLATFORM_NUDGE_WALKING_PATH.add(Wall(77.8/80*WIDTH, 5/12.2*HEIGHT, 500, 3/12.2*HEIGHT))
        PLATFORM_NUDGE_BOTH.add(Wall(77.8/80*WIDTH, 5/12.2*HEIGHT, 500, 3/12.2*HEIGHT))

        # Bench
        PLATFORM.add(Bench(64.4/80*WIDTH, 6.2/12.2*HEIGHT, 5.3/80*WIDTH, 0.7/12.2*HEIGHT))
        PLATFORM_NUDGE_BENCH.add(Bench(64.4/80*WIDTH, 6.2/12.2*HEIGHT, 5.3/80*WIDTH, 0.7/12.2*HEIGHT))
        PLATFORM_NUDGE_WALKING_PATH.add(Bench(64.4/80*WIDTH, 6.2/12.2*HEIGHT, 5.3/80*WIDTH, 0.7/12.2*HEIGHT))
        PLATFORM_NUDGE_BOTH.add(Bench(64.4/80*WIDTH, 6.2/12.2*HEIGHT, 5.3/80*WIDTH, 0.7/12.2*HEIGHT))

        # Stair area
        PLATFORM.add(SpawningRectangle(150, 122, 20, 80, 1))
        PLATFORM_NUDGE_BENCH.add(SpawningRectangle(150, 122, 20, 80, 1))
        PLATFORM_NUDGE_WALKING_PATH.add(SpawningRectangle(150, 122, 20, 80, 1))
        PLATFORM_NUDGE_BOTH.add(SpawningRectangle(150, 122, 20, 80, 1))

        # Nudge bench top
        PLATFORM_NUDGE_BENCH.add(Bench(33.8/80 * WIDTH, 4.7/12.2 * HEIGHT,  21.5/80 * WIDTH, 0.3/12.2*HEIGHT))
        PLATFORM_NUDGE_BOTH.add(Bench(33.8/80 * WIDTH, 4.7/12.2 * HEIGHT,  21.5/80 * WIDTH, 0.3/12.2*HEIGHT))

        # Nudge bench bottom
        PLATFORM_NUDGE_BENCH.add(Bench(33.8/80 * WIDTH, 8/12.2 * HEIGHT,  21.5/80 * WIDTH, 0.3/12.2*HEIGHT))
        PLATFORM_NUDGE_BOTH.add(Bench(33.8/80 * WIDTH, 8/12.2 * HEIGHT,  21.5/80 * WIDTH, 0.3/12.2*HEIGHT))
        
        PLATFORM.save_objects()
        PLATFORM_NUDGE_BENCH.save_objects()
        PLATFORM_NUDGE_WALKING_PATH.save_objects()
        PLATFORM_NUDGE_BOTH.save_objects()

        
        
        display.add(TOP_DANGERZONE)
        display.add(BOTTOM_DANGERZONE)
        display.add(PLATFORM_NUDGE_BOTH)
        

        while(display.active):
            display.update()
    else:
        PLATFORM.load_objects()
        PLATFORM_NUDGE_BENCH.load_objects()
        PLATFORM_NUDGE_WALKING_PATH.load_objects()
        PLATFORM_NUDGE_BOTH.load_objects()

def InDangerZone(position: tuple) -> bool:
    return TOP_DANGERZONE.containsPoint(position) or BOTTOM_DANGERZONE.containsPoint(position)

setup()