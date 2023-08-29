import numpy as np
from common.link import Link

class Utils:
    """Isometric Utils"""
    def __init__(self) -> None:
        self.__detect_info: list = []

    def _isometric_transform(self, points):
        """isometric transform"""
        transform_matrix = np.array([
            [1, -1, 0],
            [np.sqrt(2)/2, np.sqrt(2)/2, -np.sqrt(2)]
        ]) * np.sqrt(1/3)
        return np.dot(points, transform_matrix.T)

    def line_detect(self, pose_results):
        """line_detect"""
        pare_results = self._facing_each_other(pose_results)
        results = self._remain_pipe(pare_results, pose_results)
        return results
    
    def _remain_coordinates(self, results, pose_results, word):
        if 'downward' == word:
            up_num = next((i for i, result in enumerate(results) if 'upward' in result[2]), None)
            # print(up_num)
            if up_num is not None:
                _a = (pose_results[results[up_num][0]].position[1] - pose_results[results[up_num][1]].position[1]) / (pose_results[results[up_num][0]].position[0] - pose_results[results[up_num][1]].position[0])
                _b = pose_results[results[up_num][0]].position[1] - _a * pose_results[results[up_num][0]].position[0]
                line = (pose_results[results[up_num][0]].position[0], pose_results[results[up_num][0]].position[1]), (int((480 - _b) / _a), 480)
                return line
            elif results[0][2] == 'forward':
                line = (pose_results[results[0][0]].position[0], pose_results[results[0][0]].position[1]), (pose_results[results[0][0]].position[0], 480)
                return line
        elif 'upward' == word:
            up_num = next((i for i, result in enumerate(results) if 'downward' in result[2]), None)
            if up_num is not None:
                _a = (pose_results[results[up_num][0]].position[1] - pose_results[results[up_num][1]].position[1]) / (pose_results[results[up_num][0]].position[0] - pose_results[results[up_num][1]].position[0])
                _b = pose_results[results[up_num][0]].position[1] - _a * pose_results[results[up_num][0]].position[0]
                line = (pose_results[results[up_num][0]].position[0], pose_results[results[up_num][0]].position[1]), (int((0 - _b) / _a), 0)
                return line
            elif results[0][2] == 'forward':
                line = (pose_results[results[0][0]].position[0], pose_results[results[0][0]].position[1]), (pose_results[results[0][0]].position[0], 0)
                return line
        else:
            _a = pose_results[results[0][0]].r_matrix[1][1] / pose_results[results[0][0]].r_matrix[0][1]
            _b = pose_results[results[0][0]].position[1] - _a * pose_results[results[0][0]].position[0]
            line = (pose_results[results[0][0]].position[0], pose_results[results[0][0]].position[1]), (0, int(_b))
            return line
                
    def _decide_coordinates(self, results, pose_results, line_detects):
        for result in results:
            if (pose_results[result[1]].position, pose_results[result[0]].position) not in line_detects:
                line_detects.append((pose_results[result[0]].position, pose_results[result[1]].position))
        if len(results) == pose_results[results[0][0]].pare_num:
            return line_detects
        else:
            keywords = ['forward', 'downward'] if pose_results[results[0][0]].name == 'bent' else ['forward', 'downward', 'upward']
            detectwords = [result[2] for result in results]
            keywords = [k for k in keywords if k not in detectwords]
            for word in keywords:
                line = self._remain_coordinates(results, pose_results, word)
                if line[::-1] not in line_detects:
                    line_detects.append(line)
        return line_detects
    
    def _remain_pipe(self, pare_resutls, pose_results):
        """remain pipe"""
        line_detects = []
        for results in pare_resutls:
            line_detects = self._decide_coordinates(results, pose_results, line_detects)
        return line_detects

    def _facing_each_other(self, pose_results, threshold_angle=35) -> list:
        """find facing pipe"""
        self.__detect_info = []
        pare_results = [[] for _ in range(len(pose_results))]
        for _p1 in pose_results:
            for relationship in ['forward', 'upward']:
                for _p2 in pose_results:
                    if _p1.detection_num == _p2.detection_num or (_p2.detection_num, _p1.detection_num) in self.__detect_info:
                        continue
                    if relationship == 'forward':
                        direction1 = _p1.r_matrix[:, 0] if _p1.name == "bent" else -_p1.r_matrix[:, 1]
                        direction2 = _p2.r_matrix[:, 0] if _p2.name == "bent" else -_p2.r_matrix[:, 1]
                    else:
                        direction1 = _p1.r_matrix[:, 1] if _p1.name == "bent" else _p1.r_matrix[:, 2]
                        direction2 = -_p2.r_matrix[:, 2] if _p2.name == "bent" else -_p2.r_matrix[:, 2]
                    vector_between_objects = np.subtract(_p2.t_matrix, _p1.t_matrix).reshape(-1)
                    vector_between_objects /= np.linalg.norm(vector_between_objects)
                    angle1 = np.arccos(np.clip(np.dot(direction1, vector_between_objects), -1.0, 1.0)) * (180 / np.pi)
                    angle2 = np.arccos(np.clip(np.dot(direction2, -vector_between_objects), -1.0, 1.0)) * (180 / np.pi)
                    
                    if angle1 < threshold_angle and angle2 < threshold_angle:
                        self.__detect_info.append((_p1.detection_num, _p2.detection_num))
                        if relationship == 'forward':
                            pare_results[_p1.detection_num].append((_p1.detection_num, _p2.detection_num, relationship))
                            pare_results[_p2.detection_num].append((_p2.detection_num, _p1.detection_num, relationship))
                        else:
                            pare_results[_p1.detection_num].append((_p1.detection_num, _p2.detection_num, relationship))
                            pare_results[_p2.detection_num].append((_p2.detection_num, _p1.detection_num, 'downward'))                            
                        break
        return pare_results
            
