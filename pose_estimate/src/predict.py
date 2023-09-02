import argparse
import subprocess
import math
from pathlib import Path

import numpy as np
from skimage.io import imsave, imread

from pose_estimate.dataset.database import parse_database_name, get_ref_point_cloud
from pose_estimate.src.estimator import name2estimator
from pose_estimate.src.eval import visualize_intermediate_results
from pose_estimate.utils.base_utils import load_cfg, project_points
from pose_estimate.utils.draw_utils import pts_range_to_bbox_pts, draw_bbox_3d, draw_bbox_3d_summary
from pose_estimate.utils.pose_utils import pnp
from scipy.spatial.transform import Rotation as R

from common.pipe import Pipe

class Pose:
    def __init__(self, cfg):
        self.cfg = cfg
        self.__output_dir = Path(self.cfg['pose']['output_path'])
        self.__output_dir.mkdir(exist_ok=True, parents=True)
        
        (self.__output_dir / 'images_out').mkdir(exist_ok=True, parents=True)
        (self.__output_dir / 'images_inter').mkdir(exist_ok=True, parents=True)

        self.__estimator = []
        self.__object_bbox_3d = []
        
        for class_name in self.cfg['class_name']:
            estimator = name2estimator[self.cfg['pose']['type']](self.cfg['pose'])
            estimator.build(parse_database_name('datasets/'+class_name), split_type='all')
            object_bbox_3d = pts_range_to_bbox_pts(np.max(get_ref_point_cloud(parse_database_name('datasets/'+class_name)),0), np.min(get_ref_point_cloud(parse_database_name('datasets/'+class_name)),0))
            self.__estimator.append(estimator)
            self.__object_bbox_3d.append(object_bbox_3d)

    def predict(self, results: Pipe):
        points = []
        pose_results = []
        for i, result in enumerate(results):
            self.img = imread(self.cfg['detect']['rgb_path'] + self.cfg['input_name'])
            h, w, _ = self.img.shape
            f=np.sqrt(h**2+w**2)
            K = np.asarray([[f,0,w/2],[0,f,h/2],[0,0,1]],np.float32)
            pose_pr, inter_results = self.__estimator[result.class_num].predict(self.img, result, K, pose_init=None)
            pts, _ = project_points(self.__object_bbox_3d[result.class_num], pose_pr, K)
            imsave(f'{str(self.__output_dir)}/images_inter/{i}.jpg', visualize_intermediate_results(self.img, K, inter_results, self.__estimator[result.class_num].ref_info, self.__object_bbox_3d[result.class_num]))
            rotation = R.from_matrix(pose_pr[:, 0:3])
            roll, pitch, yaw = rotation.as_euler('zyx', degrees=True)
            pose_result = Pipe(name=result.name, position=result.position, size=result.size, pose=(roll, pitch, yaw), detection_num=i, rt_matrix=pose_pr)
            pose_results.append(pose_result)
            points.append(pts)

        bbox_img = draw_bbox_3d_summary(self.img, points, (0,0,255))
        imsave(f'{str(self.__output_dir)}/images_out/{0}-bbox.jpg', bbox_img)

        return pose_results