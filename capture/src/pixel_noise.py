import pyrealsense2 as rs
import numpy as np

# RealSenseパイプラインの初期化
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# パイプラインを開始
pipeline.start(config)

try:
    # ピクセルごとの計測データを保持するリスト
    pixel_data = []

    # 深度データを取得して処理
    for _ in range(3):  # 3回の計測
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        # ピクセルごとの距離計測値を収集
        pixel_values = np.zeros((depth_frame.height, depth_frame.width))
        for y in range(depth_frame.height):
            for x in range(depth_frame.width):
                pixel_values[y, x] = depth_frame.get_distance(x, y)

        pixel_data.append(pixel_values)

    # 各ピクセルの平均値と標準偏差を計算
    for i, pixel_values in enumerate(pixel_data):
        mean_distance = np.mean(pixel_values)
        std_deviation = np.std(pixel_values)
        print(f"Pixel {i+1}: Mean = {mean_distance}, Standard Deviation = {std_deviation}")

finally:
    # パイプラインを停止してリソースを解放
    pipeline.stop()
