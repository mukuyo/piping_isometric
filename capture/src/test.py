import pyrealsense2 as rs
import numpy as np
import cv2
from pathlib import Path
import keyboard
import wait
import time
import math
output_dir_color = Path("data/rgb/Color39")
output_dir_color.mkdir(exist_ok=True)
output_dir_depth = Path("data/depth/Depth39")
output_dir_depth.mkdir(exist_ok=True)

# colorizer = rs.colorizer()
# colorizer.set_option(rs.option.visual_preset, 0) # 0=Dynamic, 1=Fixed, 2=Near, 3=Far
# colorizer.set_option(rs.option.min_distance, 0)
# colorizer.set_option(rs.option.max_distance, value_max)

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

k = cv2.waitKey(1)

try:
    count = -1
    img_num = -1
    while True:

        time.sleep(0.1)
        count = count + 1
        # フレーム待ち(Color & Depth)
        frames = pipeline.wait_for_frames()

        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        if not depth_frame or not color_frame:
            continue
        
        # depth_color_frame = rs.colorizer().colorize(depth_frame)

        #imageをnumpy arrayに
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())


        #depth imageをカラーマップに変換
        # depth_image = cv2.convertScaleAbs(depth_image, alpha=1.0)

        #画像表示
        # color_image_s = cv2.resize(color_image, (640, 480))
        # depth_colormap_s = cv2.resize(depth_image, (640, 480))
        # images = np.hstack((color_image_s, depth_colormap_s))
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', color_image)
        # cv2.imshow('RealSense', color_image_s)\
        if cv2.waitKey(1) == ord('s'):
            img_num = img_num + 1
            save_path = output_dir_color / f"{img_num}.png"
            cv2.imwrite(str(save_path), color_image)
            save_path = output_dir_depth / f"{img_num}.png"
            cv2.imwrite(str(save_path), depth_image)
                
        
        if cv2.waitKey(1) & 0xff == 27:#ESCで終了
            cv2.destroyAllWindows()
            break
        color_intr = rs.video_stream_profile(profile.get_stream(rs.stream.depth)).get_intrinsics()
        I_d = depth_frame.get_distance(320,240)
        Point_I = rs.rs2_deproject_pixel_to_point(color_intr , [320,240], I_d)
        #ロの3次元座標推定
        R_d = depth_frame.get_distance(320,100)
        Point_R = rs.rs2_deproject_pixel_to_point(color_intr , [320,100], R_d)

        #推定距離を算出
        est_range = math.sqrt((Point_I[0]-Point_R[0])*(Point_I[0]-Point_R[0]) + (Point_I[1]-Point_R[1])*(Point_I[1]-Point_R[1]) +(Point_I[2]-Point_R[2])*(Point_I[2]-Point_R[2]))
        # print(color_intr.width)
        # print(color_intr.height)
        # print(color_intr.ppx)
        # print(color_intr.ppy)
        # print(color_intr.fx)
        # print(color_intr.fy)
        # print(color_intr.model)
        # print(color_intr.coeffs)

finally:

    #ストリーミング停止
    pipeline.stop()