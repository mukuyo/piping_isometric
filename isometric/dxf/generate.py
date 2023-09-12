import ezdxf
from math import cos, sin, pi
import numpy as np

class GenDxf:
    """Generate dxf file"""
    def __init__(self, _cfg) -> None:
        self.cfg = _cfg
        self.__doc = ezdxf.new()
        dimstyle = self.__doc.dimstyles.new('custom_dimstyle')
        dimstyle.dxf.dimtxt = self.cfg['isometric']['dimtxt']
        dimstyle.dxf.dimdec = self.cfg['isometric']['dimdex']
        dimstyle.dxf.dimasz = self.cfg['isometric']['dimasz']
        dimstyle.dxf.dimblk = self.cfg['isometric']['dimblk']
        dimstyle.dxf.dimclrd = self.cfg['isometric']['dimclrd']
        dimstyle.dxf.dimclre = self.cfg['isometric']['dimclre']
        self.__msp = self.__doc.modelspace()

        self.__position = (self.cfg['isometric']['initial_position'], self.cfg['isometric']['initial_position'])
        self.__pre_position = (self.cfg['isometric']['initial_position'], self.cfg['isometric']['initial_position'])

        self.__add_degree: float = 22.5
        self.__yaw_up_rem: float = 0
        self.__yaw_down_rem: float = 0
        self.__epsilon: float = 1e-10

    def _draw_forward(self, point1: tuple, distance: float, direction: bool):
        direction_radian = pi/6
        if direction == 0:
            direction_radian *= -1
        print(direction_radian, direction)
        point2 = (int(distance*cos(direction_radian)+point1[0]), int(distance*sin(direction_radian)+point1[1]))
        self.__msp.add_line(point1, point2)
        self.__msp.add_aligned_dim(
            p1=point1,
            p2=point2,
            distance=-self.cfg['isometric']['dimdistance'],
            dimstyle="custom_dimstyle",
            ).render()
        return point2

    def _draw_forward_only(self, point: tuple, distance: float, direction: bool) -> None:
        direction_radian = pi/6
        if direction == 0:
            direction_radian *= -1
        self.__msp.add_line(point, (distance*cos(direction_radian) + point[0], distance* sin(direction_radian) + point[1]))
    
    def _draw_downward(self, point1, distance):
        point2 = (point1[0], point1[1] - distance)
        self.__msp.add_line(point1, point2)
        self.__msp.add_linear_dim(
            base=(point1[0] + self.cfg['isometric']['dimdistance'], (point1[1] + point1[1] - distance) / 2),
            p1=point1,
            p2=point2,
            angle=90,
            dimstyle="custom_dimstyle",
        ).render()
        return point2

    def _draw_downward_only(self, point, distance) -> None:
        self.__msp.add_line(point, (point[0], point[1] - distance))

    def _draw_upward(self, point1, distance):
        point2 = (point1[0], point1[1] + distance)
        self.__msp.add_linear_dim(
            base=(point1[0] + self.cfg['isometric']['dimdistance'], (point1[1] + point1[1] - distance) / 2),
            p1=point1,
            p2=point2,
            angle=90,
            dimstyle="custom_dimstyle",
        ).render()
        self.__msp.add_line(point1, point2)
        return point2

    def _draw_upward_only(self, point, distance) -> None:
        self.__msp.add_line(point, (point[0], point[1] + distance))
    
    def _degree_normalize(self, _yaw: float):
        if _yaw > 0:
            return _yaw
        else:
            return _yaw + 180

    def isometric(self, isometric_info):
        """generate isometric dxf"""
        connect_count = -1
        for result in isometric_info:
            if result.distance < self.__epsilon:
                continue
            if connect_count == -1:
                yaw = self._degree_normalize(result.yaw)
                self.__yaw_up_rem = yaw + self.__add_degree
                self.__yaw_down_rem = yaw - self.__add_degree
            connect_count += 1
            if result.relationship == 'forward':
                direction = self._degree_normalize(result.yaw) < self.__yaw_up_rem and self._degree_normalize(result.yaw) > self.__yaw_down_rem
                print(self._degree_normalize(result.yaw), self.__yaw_up_rem, self.__yaw_down_rem, direction)
                if result.name2 != 'None':
                    self.__position = self._draw_forward(point1=self.__position, distance=result.distance, direction=direction)
                else:
                    self._draw_forward_only(point=self.__pre_position, distance=result.distance, direction=direction)
            elif result.relationship == 'downward':
                if result.name2 != 'None':
                    self.__position = self._draw_downward(self.__position, result.distance)
                else:
                    self._draw_downward_only(self.__pre_position, result.distance)
            elif result.relationship == 'upward':
                if result.name2 != 'None':
                    self.__position = self._draw_upward(self.__position, result.distance)
                else:
                    self._draw_upward_only(self.__pre_position, result.distance)
            if (result.name1 == 'elbow' and connect_count == 1) or (result.name1 == 'tee' and connect_count == 2):
                self.__pre_position = self.__position
                connect_count = 0
        self.__doc.saveas(self.cfg['isometric']['output_dxf_path'])
