"""Define ConnectInfo class"""


class ConnectInfo:
    """pipe connect info"""
    def __init__(self,
                 pipe1_position: tuple,
                 pipe2_position: tuple,
                 relationship: str,
                 pipe1_name: str = 'None',
                 pipe2_name: str = 'None',
                 distance: float = 0,
                 yaw: float = 0
                 ) -> None:
        self.__pipe1_position = pipe1_position
        self.__pipe2_position = pipe2_position
        self.__relationship = relationship
        self.__pipe1_name = pipe1_name
        self.__pipe2_name = pipe2_name
        self.distance_val = distance
        self.__yaw = yaw

    @property
    def yaw(self):
        """get yaw direction"""
        return self.__yaw

    @property
    def distance(self):
        """get distance between two positions"""
        return self.distance_val

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
        if self.__pipe2_name == 'elbow':
            return 2
        elif self.__pipe2_name == 'tee':
            return 3
        else:
            return 0

    @property
    def detection_num(self):
        """get detection num"""
        if self.__pipe1_name == 'elbow':
            return 2
        elif self.__pipe1_name == 'tee':
            return 3
        else:
            return 0

    @property
    def keywords(self):
        """get keywords"""
        if self.__pipe1_name == 'elbow':
            return ['forward', 'downward']
        elif self.__pipe1_name == 'tee':
            return ['forward', 'downward', 'upward']
        else:
            return ['forward', 'downward', 'upward']
