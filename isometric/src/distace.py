"""Getting distance for between two pipes"""
import numpy as np
from math import sqrt
from cv2 import imread, IMREAD_UNCHANGED
import pyrealsense2 as rs

class Distance:
    """get distance between two pipes"""
    def __init__(self, _cfg) -> None:
        self.cfg = _cfg

    def _compute_3d_distance(self, x1, y1, x2, y2, depth_image, intrinsics):
        depth1 = depth_image[y1, x1]
        depth2 = depth_image[y2, x2]

        point1 = rs.rs2_deproject_pixel_to_point(intrinsics, [x1, y1], depth1 * 0.1)
        point2 = rs.rs2_deproject_pixel_to_point(intrinsics, [x2, y2], depth2 * 0.1)

        distance = np.linalg.norm(np.array(point1) - np.array(point2))
        return distance


    def get_info(self, trans_info):
        """get distance information"""
        depth_image = imread(self.cfg['isometric']['depth_path'] + self.cfg['input_name'], IMREAD_UNCHANGED)
        intrinsics = rs.intrinsics()
        intrinsics.width = depth_image.shape[1]
        intrinsics.height = depth_image.shape[0]
        intrinsics.ppx = 361  # Principal point x, adjust if you have this information
        intrinsics.ppy = 242  # Principal point y, adjust if you have this information
        intrinsics.fx = 470   # Focal length x, adjust for your camera
        intrinsics.fy = 470  # Focal length y, adjust for your camera
        intrinsics.model = rs.distortion.none
        intrinsics.coeffs = [0.0, 0.0, 0.0, 0.0, 0.0]

        for info in trans_info:
            distance = self._compute_3d_distance(info.position1[0], info.position1[1], info.position2[0], info.position2[1], depth_image, intrinsics)
            print(distance, info.relationship, info.position1, info.position2, info.name2)
            info.distance_val = int(distance)
        
        return trans_info
