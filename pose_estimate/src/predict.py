import argparse
import subprocess
import math
from pathlib import Path

import numpy as np
from skimage.io import imsave, imread
from tqdm import tqdm

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
        
        (self.__output_dir / 'images_raw').mkdir(exist_ok=True, parents=True)
        (self.__output_dir / 'images_out').mkdir(exist_ok=True, parents=True)
        (self.__output_dir / 'images_inter').mkdir(exist_ok=True, parents=True)

        self.estimator_bent = name2estimator[self.cfg['pose']['type']](self.cfg['pose'])
        self.estimator_t_junc = name2estimator[self.cfg['pose']['type']](self.cfg['pose'])
        self.estimator_bent.build(parse_database_name("custom/bent"), split_type='all')
        self.estimator_t_junc.build(parse_database_name("custom/t-junc"), split_type='all')

        self.object_bbox_3d_bent = pts_range_to_bbox_pts(np.max(get_ref_point_cloud(parse_database_name("custom/bent")),0), np.min(get_ref_point_cloud(parse_database_name("custom/bent")),0))
        self.object_bbox_3d_t_junc = pts_range_to_bbox_pts(np.max(get_ref_point_cloud(parse_database_name("custom/t-junc")),0), np.min(get_ref_point_cloud(parse_database_name("custom/t-junc")),0))

    def predict(self, results: Pipe):
        points = []
        pose_results = []
        for i, result in enumerate(results):
            self.img = imread(str(self.cfg['img_path']))
            h, w, _ = self.img.shape
            f=np.sqrt(h**2+w**2)
            K = np.asarray([[f,0,w/2],[0,f,h/2],[0,0,1]],np.float32)
            
            if result.name == "bent":
                pose_pr, inter_results = self.estimator_bent.predict(self.img, result, K, pose_init=None)
                pts, _ = project_points(self.object_bbox_3d_bent, pose_pr, K)
            else:
                pose_pr, inter_results = self.estimator_t_junc.predict(self.img, result, K, pose_init=None)
                pts, _ = project_points(self.object_bbox_3d_t_junc, pose_pr, K)
            if result.name == "bent":
                imsave(f'{str(self.__output_dir)}/images_inter/{i}.jpg', visualize_intermediate_results(self.img, K, inter_results, self.estimator_bent.ref_info, self.object_bbox_3d_bent))
            else:
                imsave(f'{str(self.__output_dir)}/images_inter/{i}.jpg', visualize_intermediate_results(self.img, K, inter_results, self.estimator_t_junc.ref_info, self.object_bbox_3d_t_junc))
            rotation = R.from_matrix(pose_pr[:, 0:3])
            roll, pitch, yaw = rotation.as_euler('zyx', degrees=True)
            pose_result = Pipe(class_num=result.class_num, name=result.name, position=result.position, size=result.size, pose=(roll, pitch, yaw), detection_num=i, rt_matrix=pose_pr)
            pose_results.append(pose_result)
            points.append(pts)

        bbox_img = draw_bbox_3d_summary(self.img, points, (0,0,255))
        imsave(f'{str(self.__output_dir)}/images_out/{0}-bbox.jpg', bbox_img)

        return pose_results