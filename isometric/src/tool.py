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
        results, all_results = self._remain_pipes(pare_results, pose_results)
        all_results = self._sort_results(all_results)
        return results

    def _find_connet_pipe(self, pipe_info, all_results, isometric_line):
        _pipe_info = []
        if pipe_info:
            for info in pipe_info:
                if info[4] == 'bent':
                    connect_num = 2
                elif info[4] == 'junction':
                    connect_num = 3
                else:
                    connect_num = 0
                for _ in range(connect_num):
                    same_pipe = next((t for t in all_results if t[0][0] == info[1][0]), None)
                    all_results = [t for t in all_results if t != same_pipe]
                    if not (same_pipe[0] == info[1] and same_pipe[1] == info[0]):
                        isometric_line.append(same_pipe)
                        _pipe_info.append(same_pipe)
        return _pipe_info, all_results

    def _sort_results(self, all_results):
        isometric_line = []
        pipe_info = []
        for i in range(3):
            largest_tuple = max(all_results, key=lambda x: x[0])
            all_results = [t for t in all_results if t != largest_tuple]
            pipe_info.append(largest_tuple)
            isometric_line.append(largest_tuple)
            if i == 1 and largest_tuple[3] == 'bent':
                break
        # for _ in range(6):
        while all_results:
            pipe_info, all_results = self._find_connet_pipe(pipe_info, all_results, isometric_line)
            # print(all_results)
            # print(all_results)
            
            # print()

        for i in isometric_line:
            print(i)


    
    def _remain_direction(self, results, pose_results, word):
        if 'downward' == word:
            up_num = next((i for i, result in enumerate(results) if 'upward' in result[2]), None)
            if up_num is not None:
                _a = (pose_results[results[up_num][0]].position[1] - pose_results[results[up_num][1]].position[1]) / (pose_results[results[up_num][0]].position[0] - pose_results[results[up_num][1]].position[0])
                _b = pose_results[results[up_num][0]].position[1] - _a * pose_results[results[up_num][0]].position[0]
                line = (pose_results[results[up_num][0]].position[0], pose_results[results[up_num][0]].position[1]), (int((480 - _b) / _a), 480)
                word_line = (pose_results[results[up_num][0]].position[0], pose_results[results[up_num][0]].position[1]), (int((480 - _b) / _a), 480), word, pose_results[results[up_num][0]].name, 'None'
                return line, word_line
            elif results[0][2] == 'forward':
                line = (pose_results[results[0][0]].position[0], pose_results[results[0][0]].position[1]), (pose_results[results[0][0]].position[0], 480)
                word_line = (pose_results[results[0][0]].position[0], pose_results[results[0][0]].position[1]), (pose_results[results[0][0]].position[0], 480), word, pose_results[results[0][0]].name, 'None'
                return line, word_line
        elif 'upward' == word:
            up_num = next((i for i, result in enumerate(results) if 'downward' in result[2]), None)
            if up_num is not None:
                _a = (pose_results[results[up_num][0]].position[1] - pose_results[results[up_num][1]].position[1]) / (pose_results[results[up_num][0]].position[0] - pose_results[results[up_num][1]].position[0])
                _b = pose_results[results[up_num][0]].position[1] - _a * pose_results[results[up_num][0]].position[0]
                line = (pose_results[results[up_num][0]].position[0], pose_results[results[up_num][0]].position[1]), (int((0 - _b) / _a), 0)
                word_line = (pose_results[results[up_num][0]].position[0], pose_results[results[up_num][0]].position[1]), (int((0 - _b) / _a), 0), word, pose_results[results[up_num][0]].name, 'None'
                return line, word_line
            elif results[0][2] == 'forward':
                line = (pose_results[results[0][0]].position[0], pose_results[results[0][0]].position[1]), (pose_results[results[0][0]].position[0], 0)
                word_line = (pose_results[results[0][0]].position[0], pose_results[results[0][0]].position[1]), (pose_results[results[0][0]].position[0], 0), word, pose_results[results[0][0]].name, 'None'
                return line, word_line
        else:
            _a = pose_results[results[0][0]].r_matrix[1][1] / pose_results[results[0][0]].r_matrix[0][1]
            _b = pose_results[results[0][0]].position[1] - _a * pose_results[results[0][0]].position[0]
            line = (pose_results[results[0][0]].position[0], pose_results[results[0][0]].position[1]), (0, int(_b))
            word_line = (pose_results[results[0][0]].position[0], pose_results[results[0][0]].position[1]), (0, int(_b)), word, pose_results[results[0][0]].name, 'None'
            return line, word_line
    
    def _remain_pipes(self, pare_resutls, pose_results):
        """remain pipe"""
        line_detects = []
        all_results = []
        for results in pare_resutls:
            for result in results:
                all_results.append((pose_results[result[0]].position, pose_results[result[1]].position, result[2], pose_results[result[0]].name, pose_results[result[1]].name))
                if (pose_results[result[1]].position, pose_results[result[0]].position) not in line_detects:
                    line_detects.append((pose_results[result[0]].position, pose_results[result[1]].position))
            if len(results) != pose_results[results[0][0]].pare_num:
                keywords = ['forward', 'downward'] if pose_results[results[0][0]].name == 'bent' else ['forward', 'downward', 'upward']
                detectwords = [result[2] for result in results]
                keywords = [k for k in keywords if k not in detectwords]
                for word in keywords:
                    line, word_line = self._remain_direction(results, pose_results, word)
                    all_results.append(word_line)
                    if line[::-1] not in line_detects:
                        line_detects.append(line)
        return line_detects, all_results

    def _facing_each_other(self, pose_results, threshold_angle=35) -> list:
        """find facing pipe"""
        pare_results = [[] for _ in range(len(pose_results))]
        except_judge = []
        for _p1 in pose_results:
            for relationship in ['forward', 'upward']:
                for _p2 in pose_results:
                    if _p1.detection_num == _p2.detection_num or (_p2.detection_num, _p1.detection_num) in except_judge:
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
                        except_judge.append((_p1.detection_num, _p2.detection_num))
                        if relationship == 'forward':
                            pare_results[_p1.detection_num].append((_p1.detection_num, _p2.detection_num, relationship))
                            pare_results[_p2.detection_num].append((_p2.detection_num, _p1.detection_num, relationship))
                        else:
                            pare_results[_p1.detection_num].append((_p1.detection_num, _p2.detection_num, relationship))
                            pare_results[_p2.detection_num].append((_p2.detection_num, _p1.detection_num, 'downward'))
                        break
        return pare_results
            
