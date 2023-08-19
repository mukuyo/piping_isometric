from PIL import Image, ImageDraw
import csv
import math
name = ['bent']
position = [100, 300] #x, y
pose = [0, 0, 0]  #roll, pitch, yaw
distance = [440, 280]

roll = pose[0]
pitch = pose[1]
yaw = pose[2]

resolution = [640, 480]
range = [100, 540]
im = Image.new('RGB', (resolution[0], resolution[1]), (255, 255, 255))
draw = ImageDraw.Draw(im)

def draw_straight():
    draw.line((resolution[0]/3, resolution[1]*2/3, resolution[0]*2/3, resolution[1]/3), fill=(0, 0, 0), width=1) # connect

def draw_bent(x, y, distance):
    draw.line((x, y, x, y + distance), fill=(0, 0, 0), width=1)

def draw_Tjunc():
    draw.line((resolution[0]*2/3, resolution[1]*2/3, resolution[0]*2/3, resolution[1]/3), fill=(0, 0, 0), width=1)

if yaw >= 0:
    draw_straight()
    # draw_bent(resolution[0]/3, resolution[1]*2/3, 200)
# if name[0] == 'bent':
#     print('bent detection')

im.save("./data/Image/isometric.jpg")