import numpy as np

def isometric_transform(points):
    transform_matrix = np.array([
        [1, -1, 0],
        [np.sqrt(2)/2, np.sqrt(2)/2, -np.sqrt(2)]
    ]) * np.sqrt(1/3)
    return np.dot(points, transform_matrix.T)

def are_facing_each_other():
            for pipe in pose_results:
            if pipe.name == 'bent':
                for _ in range(2):
                    
            else:
                for _ in range(3):
                    found_pipe = are_facing_each_other(pipe, pose_results)
# def are_facing_each_other(R1, t1, R2, t2, R1_name, R2_name, threshold_angle=30):
    direction1 = R1[:, 0] if R1_name == "bent" else -R1[:, 1]
    direction2 = R2[:, 0] if R2_name == "bent" else -R2[:, 1] 

    vector_between_objects = np.subtract(t2, t1).reshape(-1)
    vector_between_objects /= np.linalg.norm(vector_between_objects)
    angle1 = np.arccos(np.clip(np.dot(direction1, vector_between_objects), -1.0, 1.0)) * (180 / np.pi)
    angle2 = np.arccos(np.clip(np.dot(direction2, -vector_between_objects), -1.0, 1.0)) * (180 / np.pi)
    if angle1 < threshold_angle and angle2 < threshold_angle:
        line = (t1.T[0], t2.T[0])
        return line
    return None