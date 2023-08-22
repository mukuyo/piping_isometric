from PIL import Image, ImageDraw
from common.pipe import Pipe
import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def are_facing_each_other(R1, t1, R2, t2, R1_name, R2_name, threshold_angle=30):
    direction1 = R1[:, 0] if R1_name == "bent" else R1[:, -1]
    direction2 = R2[:, 0] if R2_name == "bent" else R2[:, -1] 

    vector_between_objects = np.subtract(t2, t1).reshape(-1)
    vector_between_objects /= np.linalg.norm(vector_between_objects)
    angle1 = np.arccos(np.clip(np.dot(direction1, vector_between_objects), -1.0, 1.0)) * (180 / np.pi)
    angle2 = np.arccos(np.clip(np.dot(direction2, -vector_between_objects), -1.0, 1.0)) * (180 / np.pi)
    print(angle1, angle2)
    return angle1 < threshold_angle and angle2 < threshold_angle

def plot_vectors(R1, t1, R2, t2):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(t1[0], t1[1], t1[2], R1[0, 2], R1[1, 2], R1[2, 2], length=5.0, color='r', label='Object1 Direction')
    ax.quiver(t2[0], t2[1], t2[2], R2[0, 2], R2[1, 2], R2[2, 2], length=5.0, color='b', label='Object2 Direction')
    vector_between_objects = np.subtract(t2, t1).reshape(-1)
    normalized_vector = vector_between_objects / np.linalg.norm(vector_between_objects)
    ax.quiver(t1[0], t1[1], t1[2], normalized_vector[0], normalized_vector[1], normalized_vector[2], length=np.linalg.norm(vector_between_objects), color='g', label='Vector between Objects')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.show()

class Isometric:
    def __init__(self, output_path) -> None:
        self.__resolution = [640, 480]
        self.__img = Image.new('RGB', (self.__resolution[0], self.__resolution[1]), (255, 255, 255))
        self.__draw = ImageDraw.Draw(self.__img)

        self.__output_dir = output_path

    def draw_straight(self, point1, point2) -> None:
        self.__draw.line((point1[0], point1[1], point2[0], point2[1]), fill=(0, 0, 0), width=1) # connect
        
    def run(self, pose_results: list) -> None:
        for p, pipe in enumerate(pose_results):
            # print(result.name, result.position, result.size, result.pose)
            # print(pipe.name)
            for i, _pipe in enumerate(pose_results):
                if pipe.detection_num == _pipe.detection_num:
                    continue

                R1 = pipe.r_matrix
                R2 = _pipe.r_matrix
                t1 = pipe.t_matrix
                t2 = _pipe.t_matrix
                result = are_facing_each_other(R1, t1, R2, t2, pipe.name, _pipe.name)
                print(pipe.position, _pipe.position, result)
                # print("Objects are facing each other:" if result else "Objects are not facing each other")

                # plot_vectors(R1, t1, R2, t2)
            # break
            print()
                
        print("Complete making piping isometric drawing!!")    
        self.__img.save(self.__output_dir)  