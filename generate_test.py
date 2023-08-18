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


def get_pipe_info() -> list:
    """get_pipe"""

    pipe_list: list = []

    pipe = Pipe('bent', (100, 100), (0, 0, -0.750492))
    pipe_list.append(pipe)
    pipe = Pipe('T-junc', (400, 50), (0, 0, 2.3911))
    pipe_list.append(pipe)
    pipe = Pipe('bent', (100, 250), (0, 0, -0.750492))
    pipe_list.append(pipe)
    pipe = Pipe('T-junc', (400, 200), (0, 0, 2.3911))
    pipe_list.append(pipe)

    # print(list)
    return pipe_list
