class Distance:
    """get distance between two pipes"""
    def __init__(self, _cfg) -> None:
        self.cfg = _cfg

    def get_info(self, trans_info):
        """get distance information"""
        for info in trans_info:
            print(self.cfg['isometric']['depth_path'] + self.cfg['input_name'])
