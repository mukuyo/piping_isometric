"""This is a generate isomeric program"""
from isometric.opencv.draw import Draw
from isometric.src.tool import Utils

class Iso(Utils):
    """Isometric class"""
    def __init__(self, cfg) -> None:
        super().__init__(cfg)
        self.cfg = cfg
        self.__draw = Draw(self.cfg)

    def generate_iso(self, pose_results: list) -> None:
        """generate_isometric"""
        pare_results = self.facing_each_other(pose_results)
        all_results = self.remain_pipes(pare_results, pose_results)
        isometric_info = self.sort_results(all_results)
        self.__draw.line_2d(isometric_info)
        self.__draw.isometric(isometric_info)
        print("Complete making piping isometric drawing!!")
