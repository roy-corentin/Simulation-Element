import pygame
from src.world import World
from src.args import WindowsInfo


def simulation_loop(world: World) -> int:
    clock: pygame.time.Clock = pygame.time.Clock()
    fps: int = 60
    run: bool = True

    while run:
        if world.handle_input() == 84:
            run = False
        world.update()
        world.draw()
        clock.tick(fps)
    return 0


def simulation(win_info: WindowsInfo) -> int:
    pygame.init()
    world = World(win_info.width, win_info.height)
    simulation_loop(world)
    pygame.quit()
    return 0
