"""This is a capturing module file"""
from pathlib import Path
import pyrealsense2 as rs
import numpy as np
import cv2
import yaml

# ストリーム(Depth/Color)の設定
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# ストリーミング開始
pipeline = rs.pipeline()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
profile = pipeline.start(config)

# Alignオブジェクト生成
align_to = rs.stream.color
align = rs.align(align_to)

if __name__ == "__main__":
    with open('./config/capture.yaml', 'r', encoding="utf8") as yml:
        cfg = yaml.safe_load(yml)

    output_dir = Path('data/capture/' + cfg['output_dir'])
    output_dir.mkdir(exist_ok=True)
    output_dir_color = Path('data/capture/' + cfg['output_dir'] + '/color')
    output_dir_color.mkdir(exist_ok=True)
    output_dir_depth = Path('data/capture/' + cfg['output_dir'] + '/depth')
    output_dir_depth.mkdir(exist_ok=True)

    img_num = -1
    while True:
        # フレーム待ち(Color & Depth)
        frames = pipeline.wait_for_frames()

        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        if not depth_frame or not color_frame:
            continue

        #imageをnumpy arrayに
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', color_image)
        if cv2.waitKey(1) == ord('s'):
            img_num = img_num + 1
            save_path = output_dir_color / f"{img_num}.png"
            cv2.imwrite(str(save_path), color_image)
            save_path = output_dir_depth / f"{img_num}.png"
            cv2.imwrite(str(save_path), depth_image)

        if cv2.waitKey(1) & 0xff == 27:#ESCで終了
            cv2.destroyAllWindows()
            break
