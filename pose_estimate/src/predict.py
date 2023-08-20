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

from common.pipe import Pipe

def weighted_pts(pts_list, weight_num=10, std_inv=10):
    weights=np.exp(-(np.arange(weight_num)/std_inv)**2)[::-1] # wn
    pose_num=len(pts_list)
    if pose_num<weight_num:
        weights = weights[-pose_num:]
    else:
        pts_list = pts_list[-weight_num:]
    pts = np.sum(np.asarray(pts_list) * weights[:,None,None],0)/np.sum(weights)
    return pts

class Pose:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--cfg', type=str, default='pose_estimate/configs/gen6d_pretrain.yaml')
        parser.add_argument('--database', type=str, default="cu")
        parser.add_argument('--output', type=str, default="pose_estimate/data/custom/test")

        # input video process
        parser.add_argument('--video', type=str, default="data/custom/video/mouse-test.mp4")
        parser.add_argument('--resolution', type=int, default=960)
        parser.add_argument('--transpose', action='store_true', dest='transpose', default=False)

        # smooth poses
        parser.add_argument('--num', type=int, default=5)
        parser.add_argument('--std', type=float, default=2.5)

        parser.add_argument('--ffmpeg', type=str, default='ffmpeg')
        self.__args = parser.parse_args()
        self.cfg = load_cfg(self.__args.cfg)

        self.__output_dir = Path(self.__args.output)
        self.__output_dir.mkdir(exist_ok=True, parents=True)

        (self.__output_dir / 'images_raw').mkdir(exist_ok=True, parents=True)
        (self.__output_dir / 'images_out').mkdir(exist_ok=True, parents=True)
        (self.__output_dir / 'images_inter').mkdir(exist_ok=True, parents=True)
        (self.__output_dir / 'images_out_smooth').mkdir(exist_ok=True, parents=True)

        self.__pose_init = None
        self.__hist_pts = []
        self.__que_id = 0

        self.__estimator = []
        self.__object_bbox_3d = []
        class_num = 2
        name = "custom/bent"

        self.estimator_bent = name2estimator[self.cfg['type']](self.cfg)
        self.estimator_junction = name2estimator[self.cfg['type']](self.cfg)
        self.estimator_bent.build(parse_database_name("custom/bent"), split_type='all')
        self.estimator_junction.build(parse_database_name("custom/junction"), split_type='all')

        self.object_bbox_3d_bent = pts_range_to_bbox_pts(np.max(get_ref_point_cloud(parse_database_name("custom/bent")),0), np.min(get_ref_point_cloud(parse_database_name("custom/bent")),0))
        self.object_bbox_3d_junction = pts_range_to_bbox_pts(np.max(get_ref_point_cloud(parse_database_name("custom/junction")),0), np.min(get_ref_point_cloud(parse_database_name("custom/junction")),0))

    def predict(self, img_path, result: Pipe):
        self.img = imread(str(img_path))
        h, w, _ = self.img.shape
        f=np.sqrt(h**2+w**2)
        K = np.asarray([[f,0,w/2],[0,f,h/2],[0,0,1]],np.float32)
        
        if result.name == "bent":
            pose_pr, inter_results = self.estimator_bent.predict(self.img, result, K, pose_init=self.__pose_init)
            pts, _ = project_points(self.object_bbox_3d_bent, pose_pr, K)
        else:
            pose_pr, inter_results = self.estimator_junction.predict(self.img, result, K, pose_init=self.__pose_init)
            pts, _ = project_points(self.object_bbox_3d_junction, pose_pr, K)
        self.__pose_init = pose_pr
        # bbox_img = draw_bbox_3d(img, pts, (0,0,255))
        # imsave(f'{str(self.__output_dir)}/images_out/{self.__que_id}-bbox.jpg', bbox_img)
        # if result.name == "bent":
        #     imsave(f'{str(self.__output_dir)}/images_inter/{self.__que_id}.jpg', visualize_intermediate_results(img, K, inter_results, self.estimator_bent.ref_info, self.object_bbox_3d_bent))
        # else:
        #     imsave(f'{str(self.__output_dir)}/images_inter/{self.__que_id}.jpg', visualize_intermediate_results(img, K, inter_results, self.estimator_junction.ref_info, self.object_bbox_3d_junction))
        # self.__hist_pts.append(pts)
        # pts_ = weighted_pts(self.__hist_pts, weight_num=self.__args.num, std_inv=self.__args.std)
        # pose_ = pnp(self.__object_bbox_3d[result.class_num], pts_, K)
        # pts__, _ = project_points(self.__object_bbox_3d[result.class_num], pose_, K)
        # bbox_img_ = draw_bbox_3d(img, pts__, (0,0,255))
        # imsave(f'{str(self.__output_dir)}/images_out_smooth/{self.__que_id}-bbox.jpg', bbox_img_)

        roll = math.atan2(pose_pr[1][0], pose_pr[0][0])
        pitch = math.asin(-pose_pr[2][0])
        yaw = math.atan2(pose_pr[2][1], pose_pr[2][2])
        pose_result = Pipe(class_num=result.class_num, name=result.name, position=result.position, size=result.size, pose=(roll, pitch, yaw))
    
        return pose_result, pts
    
    def result_desplay(self, points_results):
        bbox_img = draw_bbox_3d_summary(self.img, points_results, (0,0,255))
        imsave(f'{str(self.__output_dir)}/images_out/{self.__que_id}-bbox.jpg', bbox_img)