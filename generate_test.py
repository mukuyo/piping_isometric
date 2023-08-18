def get_pipe_info():

    list = [] 

    name = ['bent']
    position = [100, 300]  #x, y
    pose = [0, 0, 2.3911]  #roll, pitch, yaw
    pipe_info = [name, position, pose]
    list.append(pipe_info)

    name = ['T-junc']
    position = [100, 300]     #x, y
    pose = [0, 0, -0.750492]  #roll, pitch, yaw
    pipe_info = [name, position, pose]
    list.append(pipe_info)

    print(list)
    return list