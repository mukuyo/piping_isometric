from PIL import Image, ImageDraw
from common.pipe import Pipe
import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def isometric_transform(points):
    transform_matrix = np.array([
        [1, -1, 0],
        [np.sqrt(2)/2, np.sqrt(2)/2, -np.sqrt(2)]
    ]) * np.sqrt(1/3)
    return np.dot(points, transform_matrix.T)

def are_facing_each_other(R1, t1, R2, t2, R1_name, R2_name, threshold_angle=30):
    direction1 = R1[:, 0] if R1_name == "bent" else -R1[:, 1]
    direction2 = R2[:, 0] if R2_name == "bent" else -R2[:, 1] 

    vector_between_objects = np.subtract(t2, t1).reshape(-1)
    vector_between_objects /= np.linalg.norm(vector_between_objects)
    angle1 = np.arccos(np.clip(np.dot(direction1, vector_between_objects), -1.0, 1.0)) * (180 / np.pi)
    angle2 = np.arccos(np.clip(np.dot(direction2, -vector_between_objects), -1.0, 1.0)) * (180 / np.pi)
    if angle1 < threshold_angle and angle2 < threshold_angle:
        line = (t1.T[0], t2.T[0])
        return line
    return None

class Isometric:
    def __init__(self, cfg) -> None:
        self.cfg = cfg

        self.__resolution = [640, 480]
        self.__img = Image.new('RGB', (self.__resolution[0], self.__resolution[1]), (255, 255, 255))
        self.__draw = ImageDraw.Draw(self.__img)

        self.__output_path = self.cfg['isometric']['output_path']

    def draw_straight(self, point1, point2) -> None:
        self.__draw.line((point1[0], point1[1], point2[0], point2[1]), fill=(0, 0, 0), width=1) # connect
        
    def run(self, pose_results: list) -> None:
        lines = []
        for p, pipe in enumerate(pose_results):
            for i, _pipe in enumerate(pose_results):
                if pipe.detection_num == _pipe.detection_num:
                    continue

                line = are_facing_each_other(pipe.r_matrix, pipe.t_matrix, _pipe.r_matrix, _pipe.t_matrix, pipe.name, _pipe.name)
                print(pipe.position, _pipe.position)
       
        print("Complete making piping isometric drawing!!")    
        self.__img.save(self.__output_path)  