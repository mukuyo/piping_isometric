from PIL import Image, ImageDraw
import math
from generate_test import get_pipe_info

resolution = [640, 480]
range = [100, 540]
im = Image.new('RGB', (resolution[0], resolution[1]), (255, 255, 255))
draw = ImageDraw.Draw(im)


def draw_straight() -> None:
    draw.line((resolution[0]/3, resolution[1]*2/3, resolution[0]*2/3, resolution[1]/3), fill=(0, 0, 0), width=1) # connect


def draw_bent(x, y, distance) -> None:
    draw.line((x, y, x, y + distance), fill=(0, 0, 0), width=1)


def draw_Tjunc() -> None:
    draw.line((resolution[0]*2/3, resolution[1]*2/3, resolution[0]*2/3, resolution[1]/3), fill=(0, 0, 0), width=1)


pipe_info: list = get_pipe_info()
pipe_num: int = len(pipe_info)

for pipe in pipe_info:
    print(pipe.name)
    # if pipe
    # print(pipe[2][2])

# if yaw >= 0:
    # draw_straight()
    # draw_bent(resolution[0]/3, resolution[1]*2/3, 200)
# if name[0] == 'bent':
#     print('bent detection')

# im.save("./data/Image/isometric.jpg")