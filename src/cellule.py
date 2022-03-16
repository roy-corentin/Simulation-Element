class Cellule:
    def __init__(self, color: str) -> None:
        self.color: str = color
        self.blocked: bool = False
        self.updated: bool = False

    def get_color(self) -> str:
        return self.color

    def is_blocked(self) -> bool:
        return self.blocked


class Empty(Cellule):
    def __init__(self, color: str = "black") -> None:
        super().__init__(color)


class Sand(Cellule):
    def __init__(self, color: str = "yellow") -> None:
        super().__init__(color)


class Earth(Cellule):
    def __init__(self, color: str = "brown") -> None:
        super().__init__(color)


class Water(Cellule):
    def __init__(self, color: str = "blue") -> None:
        super().__init__(color)


class Iron(Cellule):
    def __init__(self, color: str = "gray") -> None:
        super().__init__(color)
        self.blocked = True
