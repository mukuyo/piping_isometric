class Pipe:
    """pipe_info"""
    def __init__(self, class_num: int, name: str, position: list, size: float, pose: list = [0, 0, 0]):
        self.__name: str = name
        self.__position: list[int, int] = position
        self.__size: int = size
        self.__pose: list[float, float, float] = pose
        self.__class_num: int = class_num
    @property
    def class_num(self) -> int:
        """class_num"""
        return self.__class_num
    
    @property
    def name(self) -> str:
        """name"""
        return self.__name

    @property
    def position(self) -> list:
        """position"""
        return self.__position

    @property
    def size(self) -> float:
        """size"""
        return self.__size
    
    @property
    def pose(self) -> list:
        """pose"""
        return self.__pose