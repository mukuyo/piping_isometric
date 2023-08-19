class Pipe:
    """pipe_info"""
    def __init__(self, name, position, pose):
        self.__name: str = name
        self.__position: list[int, int] = position
        self.__pose: list[float, float, float] = pose

    @property
    def name(self) -> str:
        """name"""
        return self.__name

    @property
    def position(self) -> list[int, int]:
        """position"""
        return self.__position

    @property
    def pose(self) -> list[float, float, float]:
        """pose"""
        return self.__pose