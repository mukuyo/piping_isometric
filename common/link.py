class Link:
    """pipe connection info class"""
    def __init__(self, line: list = [], relationship: str = 'pipe') -> None:
        self.__line = line
        self.__relationship = relationship
