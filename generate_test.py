class Pipe:
    """pipe_info"""
    def __init__(self, num, name, position, pose):
        self.__num = num
        self.__name: str = name
        self.__position: list[int, int] = position
        self.__pose: list[float, float, float] = pose
        self.__connect_num: int

        if name == "bent":
            self.__connect_num = 2
        elif name == "T-junc":
            self.__connect_num = 3
        else:
            self.__connect_num = 3

    @property
    def num(self) -> str:
        """num"""
        return self.__num
         
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

    @property
    def connect_num(self) -> int:
        """connect num"""
        return self.__connect_num
    

def get_pipe_info() -> list:
    """get_pipe"""

    pipe_list: list = []

    pipe = Pipe(0, 'bent', (100, 100), (0, 0, -0.750492))
    pipe_list.append(pipe)
    pipe = Pipe(1, 'T-junc', (400, 50), (0, 0, 2.3911))
    pipe_list.append(pipe)
    pipe = Pipe(2, 'bent', (100, 250), (0, 0, -0.750492))
    pipe_list.append(pipe)
    pipe = Pipe(3, 'T-junc', (400, 200), (0, 0, 2.3911))
    pipe_list.append(pipe)

    # print(list)
    return pipe_list
