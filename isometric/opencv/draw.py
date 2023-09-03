from math import pi, cos, sin
from PIL import Image, ImageDraw

class DrawImage:
    """opencv draw class"""
    def __init__(self, _cfg) -> None:
        self.cfg = _cfg
        self.__resolution = self.cfg['resolution']
        self.__img_cv = Image.new('RGB', (self.__resolution[0], self.__resolution[1]), (255, 255, 255))
        self.__img_iso = Image.new('RGB', (self.__resolution[0], self.__resolution[1]), (255, 255, 255))
        self.__cv = ImageDraw.Draw(self.__img_cv)
        self.__iso = ImageDraw.Draw(self.__img_iso)

    def _draw_straight(self, point1, point2) -> None:
        self.__cv.line((point1[0], point1[1], point2[0], point2[1]), fill=(0, 0, 0), width=1)

    def _draw_iso_forward(self, point):
        self.__iso.line((point[0], point[1], -150*cos(pi/6) + point[0], -150* sin(pi/6) + point[1]), fill=(0, 0, 0), width=1)
        return [int(-150*cos(pi/6) + point[0]), int(-150* sin(pi/6) + point[1])], point

    def _draw_iso_forward_only(self, point) -> None:
        self.__iso.line((point[0], point[1], -150*cos(pi/6) + point[0], -150* sin(pi/6) + point[1]), fill=(0, 0, 0), width=1)
    
    def _draw_iso_downward(self, point) -> int:
        self.__iso.line((point[0], point[1], point[0], point[1] + 150), fill=(0, 0, 0), width=1)
        return point[1] + 150, point

    def _draw_iso_upward(self, point) -> int:
        self.__iso.line((point[0], point[1], point[0], point[1] - 150), fill=(0, 0, 0), width=1)
        return point[1] - 150, point
    
    def _draw_iso_downward_only(self, point) -> None:
        self.__iso.line((point[0], point[1], point[0], 480), fill=(0, 0, 0), width=1)

    def _draw_iso_upward_only(self, point) -> None:
        self.__iso.line((point[0], point[1], point[0], 0), fill=(0, 0, 0), width=1)

    def line_2d(self, results) -> None:
        """line_2d"""
        for result in results:
            self._draw_straight(result.position1, result.position2)
        self.__img_cv.save(self.cfg['isometric']['output_cv_path'])
    
    def isometric(self, results) -> None:
        """isometirc drawing"""
        position = results[0].position1
        pre_position = [0, 0]
        connect_count = 0
        for result in results:
            connect_count += 1
            if result.relationship == 'forward':
                if result.name2 != 'None':
                    position, pre_position = self._draw_iso_forward(position)
                else:
                    self._draw_iso_forward_only(pre_position)
            elif result.relationship == 'downward':
                if result.name2 != 'None':
                    position[1], pre_position = self._draw_iso_downward(position)
                else:
                    self._draw_iso_downward_only(pre_position)
            elif result.relationship == 'upward':
                if result.name2 != 'None':
                    position[1], pre_position = self._draw_iso_upward(position)
                else:
                    self._draw_iso_upward_only(pre_position)
            if (result.name1 == 'elbow' and connect_count == 2) or (result.name1 == 'tee' and connect_count == 3):
                pre_position = position
                connect_count = 0
        self.__img_iso.save(self.cfg['isometric']['output_iso_path'])
