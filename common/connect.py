class ConnectInfo:
    """pipe connect info"""
    def __init__(self, pipe1_position, pipe2_position, relationship, pipe1_name, pipe2_name) -> None:
        self.__pipe1_position = pipe1_position
        self.__pipe2_position = pipe2_position
        self.__relationship = relationship
        self.__pipe1_name = pipe1_name
        self.__pipe2_name = pipe2_name

    @property
    def position1(self):
        """get pipe1 position"""
        return self.__pipe1_position
    @property
    def position2(self):
        """get pipe2 position"""
        return self.__pipe2_position

    @property
    def relationship(self):
        """get relationship"""
        return self.__relationship

    @property
    def name1(self):
        """get position"""
        return self.__pipe1_name

    @property
    def name2(self):
        """get pipe2 name"""
        return self.__pipe2_name
    
    @property
    def connect_num(self):
        """get connect num"""
        if self.__pipe2_name == 'bent':
            return 2
        elif self.__pipe2_name == 'junction':
            return 3
        else:
            return 0
    