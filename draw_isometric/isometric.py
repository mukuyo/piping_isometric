from PIL import Image, ImageDraw
from common.pipe import Pipe
import numpy as np
import math

class Isometric:
    def __init__(self, output_path) -> None:
        self.__resolution = [640, 480]
        self.__img = Image.new('RGB', (self.__resolution[0], self.__resolution[1]), (255, 255, 255))
        self.__draw = ImageDraw.Draw(self.__img)

        self.__output_dir = output_path

    def draw_straight(self, point1, point2) -> None:
        self.__draw.line((point1[0], point1[1], point2[0], point2[1]), fill=(0, 0, 0), width=1) # connect
        
    def run(self, pose_results: list) -> None:
        for pipe in pose_results:
            # print(result.name, result.position, result.size, result.pose)
            print(pipe.name)
            for _pipe in pose_results:
                if pipe.detection_num == _pipe.detection_num:
                    continue
                
                # V = _pipe.t_matrix - pipe.t_matrix
                # V_ = numpy.trace(numpy.dot(pipe.r_matrix.T, _pipe.r_matrix))
                # angle = numpy.arccos(numpy.clip((V_ - 1.0) / 2.0, -1.0, 1.0))
                # print(angle * 180/ 3.14)
                # V_ = numpy.dot(V_, V)
                # V_ = pipe.r_matrix.T * _pipe.r_matrix * V
                # print(V_)
                # print(_pipe.t_matrix)
                R_A = pipe.r_matrix
                R_B = _pipe.r_matrix
                t_A = pipe.t_matrix
                t_B = _pipe.t_matrix
                if self.are_objects_facing_each_other2(R_A, t_A, R_B, t_B):
                    print("r")
                    break
                
        print("Complete making piping isometric drawing!!")    
        self.__img.save(self.__output_dir)  

    def compute_angle(self, vec1, vec2):
        """2つのベクトル間の角度をラジアンで計算する"""
        dot_product = np.dot(vec1, vec2)
        magnitude_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        cos_theta = dot_product / magnitude_product
        angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))
        return angle

    def are_objects_facing_each_other2(self, R_A, t_A, R_B, t_B, threshold=0.5):
        """
        R_A, R_B: 3x3 rotation matrices for object A and B
        t_A, t_B: 3D translation vectors for object A and B
        threshold: the threshold for the dot product to determine if the objects are facing each other
        """
        # Define a direction vector pointing forward for each object.
        # Assuming the object's forward direction is along the z-axis.
        z_axis = np.array([0, 0, 1])

        # Get the actual forward direction in world coordinates for each object.
        d_A = np.dot(R_A, z_axis)
        d_B = np.dot(R_B, z_axis)

        # Compute the direction vector from object A to object B.
        v_AB = t_B - t_A

        # Normalize the vectors for accurate dot product computation
        v_AB_normalized = v_AB / np.linalg.norm(v_AB)
        d_B_normalized = d_B / np.linalg.norm(d_B)

        # Compute the dot product between v_AB and d_B.
        dot = np.dot(v_AB_normalized, d_B_normalized)

        # If dot is negative, then object A is facing object B.
        print(dot)
        return dot < -threshold
    def are_objects_facing_each_other(self, R_A, t_A, R_B, t_B, threshold_angle=np.pi / 4):
        """2つの物体が向き合っているかを判断する"""

        # 物体の正面方向ベクトルを取得
        front_vector = np.array([0, 0, 1])
        front_A = np.dot(R_A, front_vector)
        front_B = np.dot(R_B, front_vector)

        # 物体間の方向ベクトルを取得
        direction_A_to_B = t_B - t_A
        direction_B_to_A = -direction_A_to_B

        # 各物体の正面方向ベクトルと物体間の方向ベクトルの角度を計算
        angle_A = self.compute_angle(front_A, direction_A_to_B)
        angle_B = self.compute_angle(front_B, direction_B_to_A)
        print(angle_A * 180/ 3.14, angle_B * 180/ 3.14)
        if angle_A < threshold_angle and angle_B < threshold_angle:
            return True
        else:
            return False 