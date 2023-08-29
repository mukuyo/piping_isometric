from math import pi, cos, sin
from PIL import Image, ImageDraw

class Draw:
    """opencv draw class"""
    def __init__(self) -> None:
        self.__resolution = [640, 480]
        self.__img_cv = Image.new('RGB', (self.__resolution[0], self.__resolution[1]), (255, 255, 255))
        self.__img_iso = Image.new('RGB', (self.__resolution[0], self.__resolution[1]), (255, 255, 255))
        self.__cv = ImageDraw.Draw(self.__img_cv)
        self.__iso = ImageDraw.Draw(self.__img_iso)

    def _draw_straight(self, point1, point2) -> None:
        self.__cv.line((point1[0], point1[1], point2[0], point2[1]), fill=(0, 0, 0), width=1)

    def _draw_iso_forward(self, point):
        self.__iso.line((point[0], point[1], -150*cos(pi/6) + point[0], -150* sin(pi/6) + point[1]), fill=(0, 0, 0), width=1)
        return [int(-150*cos(pi/6) + point[0]), int(-150* sin(pi/6) + point[1])]

    def _draw_iso_forward_only(self, point) -> None:
        self.__iso.line((point[0], point[1], -150*cos(pi/6) + point[0], -150* sin(pi/6) + point[1]), fill=(0, 0, 0), width=1)
    
    def _draw_iso_downward(self, point) -> int:
        self.__iso.line((point[0], point[1], point[0], point[1] - 150), fill=(0, 0, 0), width=1)
        return point[1] - 150

    def _draw_iso_upward(self, point) -> int:
        self.__iso.line((point[0], point[1], point[0], point[1] + 150), fill=(0, 0, 0), width=1)
        return point[1] + 150

    def _draw_iso_downward_only(self, point) -> None:
        self.__iso.line((point[0], point[1], point[0], 480), fill=(0, 0, 0), width=1)

    def _draw_iso_upward_only(self, point) -> None:
        self.__iso.line((point[0], point[1], point[0], 0), fill=(0, 0, 0), width=1)

    def line_2d(self, results, pose_results) -> None:
        """line_2d"""
        for result in results:
            self._draw_straight(result[0], result[1])
        self.__img_cv.save('./data/isometric/results/2d_result.jpg')
    
    def isometric(self, results, pose_results) -> None:
        """isometirc drawing"""
        x: int = 0
        y: int = 0
        num: int = 2
        if results[0][3] == 'junction':
            num = 3
        # for i in range(num):
        position = [results[0][0][0], results[0][0][1]]
        for i, result in enumerate(results):
            if result[2] == 'forward':
                if result[3] != 'None':
                    position = self._draw_iso_forward(position)
                else:
                    self._draw_iso_forward_only(position)
            elif result[2] == 'downward':
                if result[3] != 'None':
                    position[1] = self._draw_iso_downward(position)
                else:
                    self._draw_iso_downward_only(position)
            elif result[2] == 'upward':
                if result[3] != 'None':
                    position[1] = self._draw_iso_upward(position)
                else:
                    self._draw_iso_upward_only(position)
            if i < num:
                position = [result[0][0], result[0][1]]
        self.__img_iso.save('./data/isometric/results/iso_result.jpg')
