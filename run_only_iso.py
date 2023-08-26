"""This is a main script"""
import yaml
import numpy as np
from isometric.src.iso import Iso
from common.pipe import Pipe

class Main:
    """Main class"""
    def __init__(self, _cfg):
        self.cfg = _cfg
        self.isometric = Iso(self.cfg)

    def run(self):
        """run program"""
        _p: list = []
        _p.append(Pipe(class_num=1, name='junction', position=(164, 341), size=1.0, rt_matrix= np.array([[0.31932, 0.94711, -0.031878, -3.4981], [-0.27967, 0.062041, -0.95809, 3.2583], [-0.90544, 0.31485, 0.28469, 18.187]])))
        _p.append(Pipe(class_num=0, name='bent', position=(524, 383), size=1.0, rt_matrix= np.array([[-0.24416, -0.81149, 0.53091, 1.9836], [0.32891, -0.58433, -0.74187, 2.2015], [0.91225, -0.0065121, 0.4095, 8.7261]])))
        _p.append(Pipe(class_num=1, name='junction', position=(288, 351), size=1.0, rt_matrix= np.array([[0.82761, -0.55829, 0.058033, -0.48548], [0.10785, 0.056707, -0.99255, 3.0618], [0.55084, 0.8277, 0.10714, 14.94]])))
        _p.append(Pipe(class_num=0, name='bent', position=(282, 34), size=1.0, rt_matrix= np.array([[-0.58768, -0.67501, 0.44609, -1.0761], [-0.10992, -0.47963, -0.87056, -3.563], [0.8016, -0.56064, 0.20767, 16.448]])))
        _p.append(Pipe(class_num=1, name='junction', position=(179, 75), size=1.0, rt_matrix= np.array([[0.74974, -0.6556, 0.08987, -3.2378], [0.15118, 0.037475, -0.9878, -2.8712], [0.64423, 0.75418, 0.12721, 19.064]])))
        self.isometric.generate_iso(_p)

if __name__ == "__main__":
    with open('./config/main.yaml', 'r', encoding="utf8") as yml:
        cfg = yaml.safe_load(yml)

    print("init model")
    main = Main(cfg)

    print("start predict")
    main.run()
