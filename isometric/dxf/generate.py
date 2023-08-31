import ezdxf
from math import cos, sin, pi

class GenDxf:
    def __init__(self, _cfg) -> None:
        self.cfg = _cfg

        self.__doc = ezdxf.new('R2010')
        self.__msp = self.__doc.modelspace()

    def _draw_forward(self, point):
        self.__msp.add_line(point, (-150*cos(pi/6) + point[0], -150* sin(pi/6) + point[1]))
        return [int(-150*cos(pi/6) + point[0]), int(-150* sin(pi/6) + point[1])], point

    def _draw_forward_only(self, point) -> None:
        self.__msp.add_line(point, (-150*cos(pi/6) + point[0], -150* sin(pi/6) + point[1]))
    
    def _draw_downward(self, point) -> int:
        self.__msp.add_line(point, (point[0], point[1] + 150))
        return point[1] + 150, point

    def _draw_upward(self, point) -> int:
        self.__msp.add_line(point, (point[0], point[1] - 150))
        return point[1] - 150, point
    
    def _draw_downward_only(self, point) -> None:
        self.__msp.add_line(point, (point[0], 480))

    def _draw_upward_only(self, point) -> None:
        self.__msp.add_line(point, (point[0], 0))

    def isometric(self, isometric_info):
        """generate isometric dxf"""
        position = isometric_info[0].position1
        pre_position = [0, 0]
        connect_count = 0
        for result in isometric_info:
            connect_count += 1
            if result.relationship == 'forward':
                if result.name2 != 'None':
                    position, pre_position = self._draw_forward(position)
                else:
                    self._draw_forward_only(pre_position)
            elif result.relationship == 'downward':
                if result.name2 != 'None':
                    position[1], pre_position = self._draw_downward(position)
                else:
                    self._draw_downward_only(pre_position)
            elif result.relationship == 'upward':
                if result.name2 != 'None':
                    position[1], pre_position = self._draw_upward(position)
                else:
                    self._draw_upward_only(pre_position)
            if (result.name1 == 'bent' and connect_count == 2) or (result.name1 == 'junction' and connect_count == 3):
                pre_position = position
                connect_count = 0
        self.__doc.saveas(self.cfg['isometric']['output_dxf_path'])
