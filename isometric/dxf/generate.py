import ezdxf
from math import cos, sin, pi

class GenDxf:
    """Generate dxf file"""
    def __init__(self, _cfg) -> None:
        self.cfg = _cfg
        self.__doc = ezdxf.new()
        dimstyle = self.__doc.dimstyles.new('custom_dimstyle')
        dimstyle.dxf.dimtxt = 30
        dimstyle.dxf.dimdec = 0
        dimstyle.dxf.dimasz = 20.0  # 矢印のサイズを0.18に設定
        dimstyle.dxf.dimblk = 'DOT'
        dimstyle.dxf.dimclrd = 1
        self.__msp = self.__doc.modelspace()

    def _draw_forward(self, point1, distance):
        point2 = (int(distance*cos(pi/6)+point1[0]), int(distance*sin(pi/6)+point1[1]))
        self.__msp.add_line(point1, point2)
        self.__msp.add_aligned_dim(
            p1=point1,
            p2=point2,
            distance=-25,
            dimstyle="custom_dimstyle",
            ).render()
        return point2

    def _draw_forward_only(self, point, distance) -> None:
        self.__msp.add_line(point, (distance*cos(pi/6) + point[0], distance* sin(pi/6) + point[1]))
    
    def _draw_downward(self, point1, distance):
        point2 = (point1[0], point1[1] - distance)
        self.__msp.add_line(point1, point2)
        self.__msp.add_linear_dim(
            base=(point1[0] + 25, (point1[1] + point1[1] - distance) / 2),
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
            base=(point1[0] + 25, (point1[1] + point1[1] - distance) / 2),
            p1=point1,
            p2=point2,
            angle=90,
            dimstyle="custom_dimstyle",
        ).render()
        self.__msp.add_line(point1, point2)
        return point2

    def _draw_upward_only(self, point, distance) -> None:
        self.__msp.add_line(point, (point[0], point[1] + distance))

    def isometric(self, isometric_info):
        """generate isometric dxf"""
        # position = isometric_info[0].position1
        position = (100, 100)
        pre_position = (100, 100)
        connect_count = -1
        for result in isometric_info:
            connect_count += 1
            if result.relationship == 'forward':
                if result.name2 != 'None':
                    position = self._draw_forward(position, result.distance)
                else:
                    self._draw_forward_only(pre_position, result.distance)
            elif result.relationship == 'downward':
                if result.name2 != 'None':
                    position = self._draw_downward(position, result.distance)
                else:
                    self._draw_downward_only(pre_position, result.distance)
            elif result.relationship == 'upward':
                if result.name2 != 'None':
                    position = self._draw_upward(position, result.distance)
                else:
                    self._draw_upward_only(pre_position, result.distance)
            if (result.name1 == 'elbow' and connect_count == 1) or (result.name1 == 'tee' and connect_count == 2):
                pre_position = position
                connect_count = 0
        self.__doc.saveas(self.cfg['isometric']['output_dxf_path'])
