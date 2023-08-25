from PIL import Image, ImageDraw
# from common.pipe import Pipe
import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# # import numpy as np
# # import math
# # import matplotlib
# # matplotlib.use('TkAgg')

# # import matplotlib.pyplot as plt
# # from mpl_toolkits.mplot3d import Axes3D

# # # [    -3.0566     -13.547] [    -0.1074     -6.8559]
# # # [     2.0085     -17.958] [   -0.31417     -22.205]
# # # [   -0.31417     -22.205] [     2.0085     -17.958]
# # # lines_iso = [[np.array(-3.0566, -13.547)], [np.array(-0.1074 , -6.8559)]]
# # # lines_iso = [np.array((-3.0566, -13.547), dtype=float), np.array((-3.0566, -13.547), dtype=float)]
# # # lines_iso.append([np.array((2.0085, -17.958), dtype=float), np.array((-0.31417, -22.205), dtype=float)])
# # # print(lines_iso)
# # plt.figure(figsize=(10, 10))
# # # for start_iso, end_iso in lines_iso:
# # #     print(start_iso, end_iso)
# # plt.plot([-3.0566, -13.547], [-3.0566, -13.547])
# # plt.plot([2.0085, -17.958], [-0.31417, -22.205])
# # plt.title("Isometric Projection of 3D Lines")
# # plt.axis('equal')  # これが重要で
# # plt.show()  
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# # 6本の配管の座標を示すサンプルデータ
# # ここでは、(x1, y1, z1)から(x2, y2, z2)への線を表すタプルをリストとして与えています。
# pipes = [
#     ((0, 0, 0), (0, 1, 0)),
#     # ((1, 0, 0), (1, 1, 0)),
#     # ((1, 1, 0), (2, 1, 0)),
#     # ((2, 1, 0), (2, 1, 1)),   # 4本目
#     # ((2, 1, 1), (2, 2, 1)),   # 5本目
#     # ((2, 2, 1), (3, 2, 1)),   # 6本目
    
#     # 以下、他の3本の配管の座標を追加してください。
# ]

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# for pipe in pipes:
#     x = [pipe[0][0], pipe[1][0]]
#     y = [pipe[0][1], pipe[1][1]]
#     z = [pipe[0][2], pipe[1][2]]
#     ax.plot(x, y, z)
# ax.set_xlim(-0.5,3)
# ax.set_ylim(-0.5,3)
# ax.set_zlim(-0.5,3)

# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# # plt.box(False)
# # fig.patch.set_alpha(0)
# # ax.grid(False)
# # ax.set_xticks([])
# # ax.set_yticks([])
# # ax.set_zticks([])
# plt.show()
# import numpy as np
# import matplotlib.pyplot as plt

# def isometric_transform(x, y, z):
#     x_iso = x - y
#     y_iso = -x/2 - y/2 + z
#     return x_iso, y_iso

# # ボックスの座標
# box = [
#     [0, 0, 0], [5, 0, 0], [5, 5, 0], [0, 5, 0],
#     [0, 0, 5], [5, 0, 5], [5, 5, 5], [0, 5, 5]
# ]

# # 4本の線の座標
# line1_start, line1_end = (0,0,0), (3,0,0)
# line2_start, line2_end = (0,5,0), (5,0,5)
# line3_start, line3_end = (1,2,3), (4,3,2)
# line4_start, line4_end = (2,4,1), (3,1,4)

# lines = [(line1_start, line1_end)]

# box_iso = [isometric_transform(*point) for point in box]
# lines_iso = [(isometric_transform(*start), isometric_transform(*end)) for start, end in lines]

# fig, ax = plt.subplots()

# # ボックスを描画
# # ax.plot([box_iso[0][0], box_iso[1][0], box_iso[2][0], box_iso[3][0], box_iso[0][0]],
# #         [box_iso[0][1], box_iso[1][1], box_iso[2][1], box_iso[3][1], box_iso[0][1]], 'k-')
# # ax.plot([box_iso[4][0], box_iso[5][0], box_iso[6][0], box_iso[7][0], box_iso[4][0]],
# #         [box_iso[4][1], box_iso[5][1], box_iso[6][1], box_iso[7][1], box_iso[4][1]], 'k-')
# # for i in range(4):
# #     ax.plot([box_iso[i][0], box_iso[i+4][0]], [box_iso[i][1], box_iso[i+4][1]], 'k-')

# # 線を描画
# colors = ['b', 'r', 'g', 'm']
# for i, (start, end) in enumerate(lines_iso):
#     ax.plot([start[0], end[0]], [start[1], end[1]], colors[i] + '-')

# # ax.set_aspect('equal')
# ax.set_xlim(-0.5, 5)
# ax.set_ylim(-0.5, 5)
# ax.grid(True)
# # ax.spines['right'].set_position('zero') 
# plt.show()

class Isometric:
    def __init__(self, output_path) -> None:
        self.__resolution = [600, 400]
        self.__img = Image.new('RGB', (self.__resolution[0], self.__resolution[1]), (255, 255, 255))
        self.__draw = ImageDraw.Draw(self.__img)

        self.__output_dir = output_path

    def draw_straight(self, point1, point2) -> None:
        # point1 = point1[0] * math.cos(30)
        # point2 = point2 * math.sin(30)
        self.__draw.line((self.__resolution[0] - point1[0] - 100, self.__resolution[1] - point1[1] - 66, self.__resolution[0] - point2[0] - 100, self.__resolution[1] - point2[1] - 66), fill=(0, 0, 0), width=1) # connect
        
    def run(self) -> None:
        lines = []
        self.draw_straight((0.0, 0.0), (170.0 * math.cos(math.pi/6), 170.0 * math.sin(math.pi/6)))
        self.draw_straight((0.0, 0.0), (0, -100))
        self.draw_straight((170.0 * math.cos(math.pi/6), 170.0 * math.sin(math.pi/6)), (170.0 * math.cos(math.pi/6), 250))
        self.draw_straight((170.0 * math.cos(math.pi/6), 170.0 * math.sin(math.pi/6)), (170.0 * math.cos(math.pi/6), -100))
        self.draw_straight((170.0 * math.cos(math.pi/6), 250), ( 170.0 * math.cos(math.pi/6) + 150.0 * math.cos(math.pi/6), 250 + 150.0 * math.sin(math.pi/6)))
        self.draw_straight(( 170.0 * math.cos(math.pi/6) + 150.0 * math.cos(math.pi/6), 250 + 150.0 * math.sin(math.pi/6)), ( 170.0 * math.cos(math.pi/6) + 150.0 * math.cos(math.pi/6), 120))
        self.draw_straight(( 170.0 * math.cos(math.pi/6) + 150.0 * math.cos(math.pi/6), 250 + 150.0 * math.sin(math.pi/6)), ( 170.0 * math.cos(math.pi/6) + 150.0 * math.cos(math.pi/6), -100))
        self.draw_straight((280, 140), (500, 100))
        self.__img.save(self.__output_dir)  

iso = Isometric(output_path = "i.jpg")
iso.run()