import numpy as np
from common.connect import ConnectInfo

class Trans:
    """Isometric Tools"""
    def __init__(self, cfg) -> None:
        self.cfg = cfg
        self.__isometric_results = []

    def find_connet_pipe(self, pipe_info, all_results, isometric_line):
        """find connect pipe"""
        _pipe_info = []
        for info in pipe_info:
            for _ in range(info.connect_num):
                same_pipe = next((t for t in all_results if t.position1[0] == info.position2[0]), None)
                all_results = [t for t in all_results if t != same_pipe]
                if not (same_pipe.position1 == info.position2 and same_pipe.position2 == info.position1):
                    isometric_line.append(same_pipe)
                    _pipe_info.append(same_pipe)
        return _pipe_info, all_results, isometric_line

    def sort_results(self, all_results):
        """sort results"""
        isometric_line = []
        pipe_info = []
        for i in range(3):
            largest_tuple = min(all_results, key=lambda x: x.position1[0])
            all_results = [t for t in all_results if t != largest_tuple]
            pipe_info.append(largest_tuple)
            isometric_line.append(largest_tuple)
            if i == 1 and largest_tuple.name1 == 'elbow':
                break
        while all_results:
            pipe_info, all_results, isometric_line = self.find_connet_pipe(pipe_info, all_results, isometric_line)

        return isometric_line

    def remain_direction(self, results, pose_results, word):
        """remain direction"""
        if 'downward' == word:
            up_num = next((i for i, result in enumerate(results) if 'upward' in result.relationship), None)
            if up_num is not None:
                _a = (results[up_num].position1[1] - results[up_num].position2[1]) / (results[up_num].position1[0] - results[up_num].position2[0])
                _b = results[up_num].position1[1] - _a * results[up_num].position1[0]
                line = ConnectInfo(results[up_num].position1, (int((self.cfg['resolution'][1]-1 - _b) / _a), self.cfg['resolution'][1]-1), word, results[up_num].name1, 'None')
            elif results[0].relationship == 'forward':
                line = ConnectInfo(results[0].position1, (results[0].position1[0], self.cfg['resolution'][1]-1), word, results[0].name1, 'None')
        elif 'upward' == word:
            up_num = next((i for i, result in enumerate(results) if 'downward' in result.relationship), None)
            if up_num is not None:
                _a = (results[up_num].position1[1] - results[up_num].position2[1]) / (results[up_num].position1[0] - results[up_num].position2[0])
                _b = results[up_num].position1[1] - _a * results[up_num].position1[0]
                line = ConnectInfo(results[up_num].position1, (int((0 - _b) / _a), 0), word, results[up_num].name1, 'None')
            elif results[0].relationship == 'forward':
                line = ConnectInfo(results[0].position1, (results[0].position1[0], 0), word, results[0].name1, 'None')
        else:
            _a = pose_results[results[0].detection_num].r_matrix[1][1] / pose_results[results[0].detection_num].r_matrix[0][1]
            _b = results[0].position1[1] - _a * results[0].position1[0]
            line = ConnectInfo(results[0].position1, (0, int(_b)), word, results[0].name1, 'None')
        self.__isometric_results.append(line)
        # print(line.position1, line.position2, word)
    
    def remain_pipes(self, pare_resutls, pose_results):
        """remain pipe"""
        for results in pare_resutls:
            if results:
                if len(results) != results[0].detection_num:
                    detectwords = [result.relationship for result in results]
                    remainwords = [k for k in results[0].keywords if k not in detectwords]
                    # print(results[0].keywords, detectwords, remainwords)
                    for word in remainwords:
                        self.remain_direction(results, pose_results, word)
        return self.__isometric_results

    def facing_each_other(self, pose_results) -> list:
        """find facing pipe"""
        threshold_angle = self.cfg['isometric']['threshold_angle']
        pare_results = [[] for _ in range(len(pose_results))]
        except_judge = []
        for _p1 in pose_results:
            for relationship in ['forward', 'updownward']:
                for _p2 in pose_results:
                    if _p1.detection_num == _p2.detection_num or (_p2.detection_num, _p1.detection_num) in except_judge:
                        continue
                    if relationship == 'forward':
                        direction1 = _p1.r_matrix[:, 0] if _p1.name == "elbow" else _p1.r_matrix[:, 2]
                        direction2 = _p2.r_matrix[:, 0] if _p2.name == "elbow" else _p2.r_matrix[:, 2]
                    else:
                        direction1 = _p1.r_matrix[:, 1] if _p1.name == "elbow" else _p1.r_matrix[:, 0]
                        direction2 = -_p2.r_matrix[:, 2] if _p2.name == "elbow" else _p2.r_matrix[:, 0]
                    vector_between_objects = np.subtract(_p2.t_matrix, _p1.t_matrix).reshape(-1)
                    vector_between_objects /= np.linalg.norm(vector_between_objects)
                    angle1 = np.arccos(np.clip(np.dot(direction1, vector_between_objects), -1.0, 1.0)) * (180 / np.pi)
                    angle2 = np.arccos(np.clip(np.dot(direction2, -vector_between_objects), -1.0, 1.0)) * (180 / np.pi)
                    print(angle1, angle2, relationship, _p1.position, _p2.position)
                    if abs(90 - angle1) < threshold_angle and abs(90 - angle2) < threshold_angle:
                        except_judge.append((_p1.detection_num, _p2.detection_num))
                        if relationship == 'forward':
                            line1 = ConnectInfo(_p1.position, _p2.position, relationship, pipe1_name=_p1.name, pipe2_name=_p2.name)
                            line2 = ConnectInfo(_p2.position, _p1.position, relationship, pipe1_name=_p2.name, pipe2_name=_p1.name)
                        else:
                            if _p1.position[1] < _p2.position[1]:
                                line1 = ConnectInfo(_p1.position, _p2.position, 'downward', pipe1_name=_p1.name, pipe2_name=_p2.name)
                                line2 = ConnectInfo(_p2.position, _p1.position, 'upward', pipe1_name=_p2.name, pipe2_name=_p1.name)
                            else:
                                line1 = ConnectInfo(_p1.position, _p2.position, 'upward', pipe1_name=_p1.name, pipe2_name=_p2.name)
                                line2 = ConnectInfo(_p2.position, _p1.position, 'downward', pipe1_name=_p2.name, pipe2_name=_p1.name)
                        pare_results[_p1.detection_num].append(line1)
                        pare_results[_p2.detection_num].append(line2)
                        self.__isometric_results.append(line1)
                        self.__isometric_results.append(line2)
                        break
        return pare_results
            
