from typing import Dict, List, Tuple
from src.cellule import Cellule, Earth, Empty, Sand, Water, Iron
import pygame


class World:
    def __init__(self, width: int = 800, height: int = 800) -> None:
        """WINDOWS/SURFACE"""
        self.size_win: Tuple[int, int] = (width, height)
        self.window: pygame.surface.Surface = pygame.display.set_mode(
            self.size_win, pygame.RESIZABLE, pygame.DOUBLEBUF
        )
        self.size_cell: int = 5
        self.width: int = width // self.size_cell
        self.height: int = height // self.size_cell
        """COLOR"""
        self.black: Tuple[int, int, int] = (0, 0, 0)
        self.white: Tuple[int, int, int] = (250, 250, 250)
        """CELLULE"""
        self.cellules: List[List[Cellule]] = [
            [Empty() for _ in range(self.width)] for _ in range(self.height - 1)
        ]
        self.cellules.append([Earth() for _ in range(self.width)])
        """MATERIAL"""
        self.materials: Dict = {
            "sand": self.__create_block_of_sand,
            "water": self.__create_block_of_water,
            "iron": self.__create_block_of_iron,
            "empty": self.__create_block_of_empty,
        }
        self.current_material = "sand"

    def draw(self) -> None:
        self.window.fill(self.black)
        for line, y in zip(self.cellules, range(self.height)):
            for cellule, x in zip(line, range(self.width)):
                if isinstance(cellule, Empty):
                    continue
                cellule.updated = False
                self.__draw_cell(cellule, x, y)
        pygame.display.flip()

    def update(self) -> None:
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                current_cell: Cellule = self.cellules[y][x]
                if current_cell.blocked or current_cell.updated:
                    continue
                if isinstance(current_cell, Sand):
                    self.__move_sand(x, y)
                if isinstance(current_cell, Earth):
                    self.__move_earth(x, y)
                if isinstance(current_cell, Water):
                    self.__move_water(x, y)

    def handle_input(self) -> int:
        pos: Tuple[int, int] = pygame.mouse.get_pos()
        x: int = pos[0] // self.size_cell
        y: int = pos[1] // self.size_cell
        mouse_key: Tuple[bool, bool, bool] | Tuple[
            bool, bool, bool, bool, bool
        ] = pygame.mouse.get_pressed()
        if mouse_key[0]:
            self.materials[self.current_material](x, y)
        if mouse_key[2]:
            self.materials["empty"](x, y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 84
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.current_material = "water"
                if event.key == pygame.K_s:
                    self.current_material = "sand"
                if event.key == pygame.K_i:
                    self.current_material = "iron"
        return 0

    def __draw_cell(self, cellule: Cellule, x: int, y: int) -> None:
        rect: pygame.Rect = pygame.Rect(
            x * self.size_cell,
            y * self.size_cell,
            self.size_cell,
            self.size_cell,
        )
        pygame.draw.rect(
            self.window,
            cellule.get_color(),
            rect,
        )

    def __create_block_of_sand(self, x: int, y: int) -> None:
        pos_list: List[Tuple[int, int]] = [
            (x, y),
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x + 1, y + 1),
            (x - 1, y + 1),
        ]
        for pos in pos_list:
            pos_x, pos_y = pos
            if self.__in_range(pos_x, pos_y):
                self.cellules[pos_y][pos_x] = Sand()

    def __create_block_of_water(self, x: int, y: int) -> None:
        pos_list: List[Tuple[int, int]] = [
            (x, y),
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x + 1, y + 1),
            (x - 1, y + 1),
        ]
        for pos in pos_list:
            pos_x, pos_y = pos
            if self.__in_range(pos_x, pos_y):
                self.cellules[pos_y][pos_x] = Water()

    def __create_block_of_iron(self, x: int, y: int) -> None:
        pos_list: List[Tuple[int, int]] = [
            (x, y),
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x + 1, y + 1),
            (x - 1, y + 1),
        ]
        for pos in pos_list:
            pos_x, pos_y = pos
            if self.__in_range(pos_x, pos_y):
                self.cellules[pos_y][pos_x] = Iron()

    def __create_block_of_empty(self, x: int, y: int) -> None:
        pos_list: List[Tuple[int, int]] = [
            (x, y),
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x + 1, y + 1),
            (x - 1, y + 1),
        ]
        for pos in pos_list:
            pos_x, pos_y = pos
            if self.__in_range(pos_x, pos_y):
                self.cellules[pos_y][pos_x] = Empty()

    def __move_sand(self, x: int, y: int) -> None:
        if self.__is_empty_cell_or_water(x, y + 1):
            self.__switch_cell((x, y), (x, y + 1))
        elif self.__is_empty_cell_or_water(x - 1, y + 1):
            self.__switch_cell((x, y), (x - 1, y + 1))
        elif self.__is_empty_cell_or_water(x + 1, y + 1):
            self.__switch_cell((x, y), (x + 1, y + 1))
        self.cellules[y][x].updated = True

    def __move_water(self, x: int, y: int) -> None:
        if self.__is_empty_cell(x, y + 1):
            self.__switch_cell((x, y), (x, y + 1))
        elif self.__is_empty_cell(x - 1, y + 1):
            self.__switch_cell((x, y), (x - 1, y + 1))
        elif self.__is_empty_cell(x + 1, y + 1):
            self.__switch_cell((x, y), (x + 1, y + 1))
        elif self.__is_empty_cell(x + 1, y):
            self.__switch_cell((x, y), (x + 1, y))
        elif self.__is_empty_cell(x - 1, y):
            self.__switch_cell((x, y), (x - 1, y))
        self.cellules[y][x].updated = True

    def __switch_cell(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> None:
        temp: Cellule = self.cellules[pos1[1]][pos1[0]]
        self.cellules[pos1[1]][pos1[0]] = self.cellules[pos2[1]][pos2[0]]
        self.cellules[pos2[1]][pos2[0]] = temp

    def __move_earth(self, x: int, y: int) -> None:
        if self.__is_empty_cell(x, y + 1):
            self.cellules[y][x] = Empty()
            self.cellules[y + 1][x] = Earth()

    def __is_empty_cell(self, x: int, y: int) -> bool:
        return self.__in_range(x, y) and isinstance(self.cellules[y][x], Empty)

    def __is_empty_cell_or_water(self, x: int, y: int) -> bool:
        return self.__in_range(x, y) and (
            isinstance(self.cellules[y][x], Empty)
            or isinstance(self.cellules[y][x], Water)
        )

    def __in_range(self, x: int, y: int) -> bool:
        if y >= self.height or y < 0:
            return False
        if x >= self.width or x < 0:
            return False
        return True

    def __mouse_in(self, rect: pygame.Rect) -> bool:
        pos: Tuple[int, int] = pygame.mouse.get_pos()
        return rect.collidepoint(pos)
