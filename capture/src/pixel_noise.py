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
    for _ in range(100):  # 100回のサンプリング
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        # ピクセルごとの距離計測値を収集
        pixel_values = np.zeros((depth_frame.height, depth_frame.width))
        for y in range(depth_frame.height):
            for x in range(depth_frame.width):
                pixel_values[y, x] = depth_frame.get_distance(x, y)

        pixel_data.append(pixel_values)

    # 各ピクセルの標準偏差を計算
    pixel_std_devs = np.zeros((depth_frame.height, depth_frame.width))  # 各ピクセルの標準偏差を保持する配列
    for y in range(depth_frame.height):
        for x in range(depth_frame.width):
            pixel_samples = [sample[y, x] for sample in pixel_data]
            pixel_std_devs[y, x] = np.std(pixel_samples)

    # 各ピクセルの平均標準偏差を計算
    mean_std_dev = np.mean(pixel_std_devs)
    print(f"Mean Standard Deviation: {mean_std_dev}")

finally:
    # パイプラインを停止してリソースを解放
    pipeline.stop()
