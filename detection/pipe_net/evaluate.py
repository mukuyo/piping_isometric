import argparse
from pathlib import Path

import pandas as pd
import torch
from yolov3.datasets.custom import CustomDataset
from yolov3.utils import pascalvoc_metrics, utils
from yolov3.utils.model import create_model, parse_yolo_weights
import random
import numpy as np
import time
from yolov3.datasets.linemod import LINEMODDDataset

seed = 42
random.seed(seed)
# Numpy
np.random.seed(seed)
# Pytorch
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.backends.cudnn.deterministic = True
torch.use_deterministic_algorithms = True

bent = []
junction = []
mean = []

bent_iou = []
junction_iou = []



def parse_args():
    """Parse command line arguments."""
    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_dir", type=Path, required=True,
        help="directory path to coco dataset"
    )
    parser.add_argument(
        "--output", type=Path, default="metrics_output",
        help="directory path to output metrics results",
    )
    parser.add_argument(
        "--weights", type=Path, required=True,
        help="path to weights file",
    )
    parser.add_argument(
        "--config", type=Path, default="config/yolov3_custom.yaml",
        help="path to config file",
    )
    parser.add_argument(
        "--gpu_id", type=int, default=0,
        help="GPU id to use")
    parser.add_argument(
        "--iou", type=float, default=0.5,
        help="IOU threshold")
    # fmt: on
    args = parser.parse_args()

    return args


def prediction_to_dict(no, output, class_names):
    detection = []
    for x1, y1, x2, y2, obj_conf, class_conf, class_id in output:
        bbox = {
            "No": no,
            "Score": float(obj_conf * class_conf),
            "Label": class_names[int(class_id)],
            "Xmin": float(x1),
            "Ymin": float(y1),
            "Xmax": float(x2),
            "Ymax": float(y2),
        }
        detection.append(bbox)

    return detection


def groundtruth_to_dict(no, label, class_names, pad_info, img_size):
    scale_x, scale_y, dx, dy = pad_info

    # remove label padding
    label = label[(label != 0).any(dim=1)]

    # decode bboxes
    label[:, 1:] *= img_size
    label[:, 1:3] -= torch.stack([dx, dy])
    label[:, 1:] /= torch.stack([scale_x, scale_y, scale_x, scale_y])

    groundtruth = []
    for class_id, cx, cy, w, h in label:
        x1, y1 = cx - w / 2, cy - h / 2
        x2, y2 = cx + w / 2, cy + h / 2

        bbox = {
            "No": no,
            "Label": class_names[int(class_id)],
            "Xmin": float(x1),
            "Ymin": float(y1),
            "Xmax": float(x2),
            "Ymax": float(y2),
        }
        groundtruth.append(bbox)

    return groundtruth


def output_metrics(groundtruths, predictions, class_names, iou, output_dir):
    utils.japanize_matplotlib()

    # クラスごとに計算する。
    results = []

    for class_ in class_names:
        result, iou_max = pascalvoc_metrics.calc_metrics(
            groundtruths, predictions, class_, iou_threshold=iou
        )
        results.append(result)
    # 各クラスの AP をデータフレームでまとめる。
    metrics = pascalvoc_metrics.aggregate(results)
    print(metrics)
    for result in results:
        # metrics.append({"Class": result["class"], "AP": result["average_precision"]})
        mean.append(metrics.loc["mAP"])
        if not(np.isnan(result["average_precision"])):
            if result["class"] == "bent":
                bent_iou.append(result["iou_max"])
                bent.append(result["average_precision"])
            elif result["class"] == "junction":
                junction_iou.append(result["iou_max"])
                junction.append(result["average_precision"])
    

    # 結果を出力する。
    output_dir.mkdir(exist_ok=True)
    det_bboxes = []
    for ret in results:
        save_path = output_dir / f"{ret['class']}.png"
        pascalvoc_metrics.plot_pr_curve(ret, save_path)

        det_bboxes.append(ret["det_bboxes"])

    save_path = output_dir / "detections.csv"
    det_bboxes = pd.concat(det_bboxes).sort_values("No")
    det_bboxes.to_csv(save_path, index=False)

    save_path = output_dir / f"metrics.csv"
    metrics.to_csv(save_path, index=False)


def main():
    args = parse_args()

    # 設定ファイルを読み込む。
    config = utils.load_config(args.config)
    img_size = config["test"]["img_size"]
    batch_size = config["test"]["batch_size"]
    conf_threshold = config["test"]["conf_threshold"]
    nms_threshold = config["test"]["nms_threshold"]
    class_names = utils.load_classes(
        args.config.parent / config["model"]["class_names"]
    )

    # デバイスを作成する。
    device = utils.get_device(gpu_id=args.gpu_id)

    # モデルを作成する。
    model = create_model(config)
    params = 0
    for p in model.parameters():
        if p.requires_grad:
            params += p.numel()
    print(params)
    if args.weights.suffix == ".weights":
        parse_yolo_weights(model, args.weights)
        print(f"Darknet format weights file loaded. {args.weights}")
    else:
        state = torch.load(args.weights)
        model.load_state_dict(state["model"])
        print(f"Checkpoint file {args.weights} loaded.")
    model = model.to(device).eval()
    train_dataset = LINEMODDDataset(img_size=img_size, train=False)
    # Dataset を作成する。
    # train_dataset = CustomDataset(
    #     Path('data/datasets/test_3/Color'),
    #     Path('data/datasets/test_3/Depth'),
    #     class_names,
    #     train=False,
    #     img_size=img_size,
    #     bbox_format="pascal_voc",
    # )

    # DataLoader を作成する。
    train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size)

    groundtruths = []
    predictions = []
    no = 0
    count = 0
    start = time.time()
    bent_sum2 = 0.0
    junction_sum2 = 0.0
    mean_sum2 = 0.0

    for inputs, inputs2, labels, pad_infos in train_dataloader:
        # if count == 100:
            # break
        count += 1
        inputs = inputs.to(device)
        inputs2 = inputs2.to(device)
        pad_infos = [x.to(device) for x in pad_infos]
        labels = labels.to(device)

        with torch.no_grad():
            outputs = model(inputs, inputs2)
            outputs = utils.postprocess(
                outputs, conf_threshold, nms_threshold, pad_infos
            )

            for label, output, *pad_info in zip(labels, outputs, *pad_infos):
                groundtruths += groundtruth_to_dict(
                    no, label, class_names, pad_info, img_size
                )
                predictions += prediction_to_dict(no, output, class_names)
                no += 1

    groundtruths = pd.DataFrame(groundtruths)
    predictions = pd.DataFrame(predictions)

    # 結果を出力する。
    output_metrics(groundtruths, predictions, class_names, args.iou, args.output)

    # for i in range(10):
    #     out = out + (0.5*i)

    #     for inputs, inputs2, labels, pad_infos in train_dataloader:
    #         count += 1
    #         inputs = inputs.to(device)
    #         inputs2 = inputs2.to(device)
    #         pad_infos = [x.to(device) for x in pad_infos]
    #         labels = labels.to(device)

    #         with torch.no_grad():
    #             outputs = model(inputs, inputs2)
    #             outputs = utils.postprocess(
    #                 outputs, conf_threshold, nms_threshold, pad_infos
    #             )

    #             for label, output, *pad_info in zip(labels, outputs, *pad_infos):
    #                 groundtruths = groundtruth_to_dict(
    #                     no, label, class_names, pad_info, img_size
    #                 )
    #                 predictions = prediction_to_dict(no, output, class_names)
    #                 no = 1

    #         groundtruths = pd.DataFrame(groundtruths)
    #         predictions = pd.DataFrame(predictions)

    #         # 結果を出力する。
    #         output_metrics(groundtruths, predictions, class_names, out, args.output)


    #     bent_sum = 0.0
    #     junction_sum = 0.0
    #     bent_iou_sum = 0.0
    #     junction_iou_sum = 0.0
    #     for i in range(len(bent)):
    #         bent_sum += bent[i]
    #         bent_iou_sum += bent_iou[i]

    #     for i in range(len(junction)):
    #         junction_sum += junction[i]
    #         junction_iou_sum += junction_iou[i]

    #     bent_sum /= len(bent)
    #     bent_iou_sum /= len(bent)
    #     junction_sum /= len(junction)
    #     junction_iou_sum /= len(junction)

    #     print("bent")
    #     print(bent_sum, bent_iou_sum)
    #     print("junction")
    #     print(junction_sum, junction_iou_sum)
    #     print("mean")
    #     print((bent_sum + junction_sum) / 2, (bent_iou_sum + junction_iou_sum) / 2)

    #     bent_sum2 += bent_sum
    #     junction_sum2 += junction_sum
    #     mean_sum2 += (bent_sum + junction_sum) / 2
    
    # print(bent_sum2/10, junction_sum2/10, mean_sum2/10)
    # print(time.time() - start)

if __name__ == "__main__":
    main()
