"""This is a generate isomeric program"""
# from isometric.opencv.draw import DrawImage
from isometric.dxf.generate import GenDxf
from isometric.src.transform import Trans
from isometric.src.distace import Distance


class Iso():
    """Isometric class"""
    def __init__(self, cfg, logger) -> None:
        self.__cfg = cfg
        self.__logger = logger
        self.__trans = Trans(self.__cfg)
        self.__distance = Distance(self.__cfg)
        # self.__draw = DrawImage(self.__cfg)
        self.__dxf = GenDxf(self.__cfg)

    def generate_iso(self, pose_results: list) -> None:
        """generate_isometric"""
        pare_results = self.__trans.facing_each_other(pose_results)
        if pare_results[0]:
            all_results = self.__trans.remain_pipes(pare_results, pose_results)
            sort_info = self.__trans.sort_results(all_results)
            isometric_info = self.__distance.get_info(sort_info)
            # self.__draw.line_2d(isometric_info)
            # self.__draw.isometric(isometric_info)
            self.__dxf.isometric(isometric_info)
            self.__logger.info('Complete making piping isometric drawing!!')
        else:
            self.__logger.info('Connected pipe not found')
