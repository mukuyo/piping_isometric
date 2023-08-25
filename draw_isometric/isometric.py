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
    # print(angle1, angle2)
    if angle1 < threshold_angle and angle2 < threshold_angle:
        line = (t1.T[0], t2.T[0])
        print(t1[0])
        # line = t1[0]
        return line
    return None

def plot_vectors(R1, t1, R2, t2):
    # -R1[:, 1]
    # direction2 = R2[:, 0] if R2_name == "bent" else -R2[:, 1] 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(t1[0], t1[1], t1[2], R1[2, 2], R1[1, 2], R1[2, 2], length=5.0, color='r', label='Object1 Direction')
    ax.quiver(t2[0], t2[1], t2[2], R2[2, 2], R2[1, 2], R2[2, 2], length=5.0, color='b', label='Object2 Direction')
    vector_between_objects = np.subtract(t2, t1).reshape(-1)
    normalized_vector = vector_between_objects / np.linalg.norm(vector_between_objects)
    ax.quiver(t1[0], t1[1], t1[2], normalized_vector[0], normalized_vector[1], normalized_vector[2], length=np.linalg.norm(vector_between_objects), color='g', label='Vector between Objects')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    ax.set_xlim(-8, 10)
    ax.set_ylim(-8, 5)
    ax.set_zlim(0, 20)
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
        lines = []
        for p, pipe in enumerate(pose_results):
            for i, _pipe in enumerate(pose_results):
                if pipe.detection_num == _pipe.detection_num:
                    continue

                line = are_facing_each_other(pipe.r_matrix, pipe.t_matrix, _pipe.r_matrix, _pipe.t_matrix, pipe.name, _pipe.name)
                # if p == 1 and i == 2:
                print(pipe.position, _pipe.position)
                plot_vectors(pipe.r_matrix, pipe.t_matrix, _pipe.r_matrix, _pipe.t_matrix)
                # if line is not None:
                    # lines.append(line)
                # print(pipe.position, _pipe.position, result)
            # print()
        # num_lines = 4
        # lines = [(np.random.rand(3) * 10, np.random.rand(3) * 10) for _ in range(num_lines)]

        # lines_iso = [(isometric_transform(start), isometric_transform(end)) for start, end in lines]
        # # print(lines)
        # # print(lines_iso)
        # plt.figure(figsize=(10, 10))
        # for start_iso, end_iso in lines_iso:
        #     print(start_iso, end_iso)
        #     plt.plot([start_iso[0], end_iso[0]], [start_iso[1], end_iso[1]])

        # plt.title("Isometric Projection of 3D Lines")
        # plt.axis('equal')  # これが重要で
        # plt.show()        
        print("Complete making piping isometric drawing!!")    
        self.__img.save(self.__output_dir)  