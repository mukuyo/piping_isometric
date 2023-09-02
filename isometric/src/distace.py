"""Getting distance for between two pipes"""
from math import sqrt
from cv2 import imread, IMREAD_UNCHANGED
import pyrealsense2 as rs

class Distance:
    """get distance between two pipes"""
    def __init__(self, _cfg) -> None:
        self.cfg = _cfg

    def _distance_between_two_positions(self, depth_image, intrinsics, position1, position2):
        depth_value1 = depth_image[position1[1], position1[0]]
        x_1, y_1, z_1 = rs.rs2_deproject_pixel_to_point(intrinsics, [float(position1[0]), float(position1[1])], depth_value1)

        depth_value2 = depth_image[position2[1], position2[0]]
        x_2, y_2, z_2 = rs.rs2_deproject_pixel_to_point(intrinsics, [float(position2[0]), float(position2[1])], depth_value2)

        distance = sqrt((x_2 - x_1) * (x_2 - x_1) + (y_2 - y_1) * (y_2 - y_1) + (z_2 - z_1) * (z_2 - z_1))
        return distance

    def get_info(self, trans_info):
        """get distance information"""
        depth_image = imread(self.cfg['isometric']['depth_path'] + self.cfg['input_name'], IMREAD_UNCHANGED)
        intrinsics = rs.intrinsics()
        intrinsics.width = depth_image.shape[1]
        intrinsics.height = depth_image.shape[0]
        intrinsics.ppx = intrinsics.width / 2  # Principal point x, adjust if you have this information
        intrinsics.ppy = intrinsics.height / 2  # Principal point y, adjust if you have this information
        intrinsics.fx = 7  # Focal length x, adjust for your camera
        intrinsics.fy = 7  # Focal length y, adjust for your camera

        for info in trans_info:
            distance = self._distance_between_two_positions(depth_image, intrinsics, info.position1, info.position2)
            info.distance_val = distance
        
        return trans_info
