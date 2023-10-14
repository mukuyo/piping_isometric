from collections import defaultdict

import torch
from torch import nn as nn

from ..models.yolo_layer import YOLOLayer

class RXD(nn.Module):
    def __init__(self, in_ch):
        super().__init__()

        self.conv_0 = nn.Sequential(
                                    nn.Conv2d(in_ch, in_ch//2, 1, 1, 0),
                                    nn.ReLU()
        )

        self.conv_1 = nn.Sequential(
                                    nn.Conv2d(in_ch, in_ch, 3, 1, 1),
                                    nn.Sigmoid()
        )
        self.conv_2 = nn.Sequential(
                                    nn.Conv2d(in_ch*2, in_ch*4, 3, 1, 1), 
                                    nn.ReLU()
        )
        self.conv_3 = nn.Sequential(
                                    nn.Conv2d(in_ch*4, in_ch*2, 1, 1, 0),  
                                    nn.BatchNorm2d(in_ch*2),
                                    nn.ReLU()
        )
    def forward(self, rgb, depth): #128 - 256
        rgb_1 = self.conv_0(rgb) 
        depth_1 = self.conv_0(depth) # 128
        con_1 = torch.cat((rgb_1, depth_1), dim=1) #256 
        con_1 = self.conv_1(con_1)
        rgb_mul = torch.mul(rgb, con_1) 
        depth_mul = torch.mul(depth, con_1) #256

        con_1 = torch.cat((rgb_mul, depth_mul), dim=1) #512

        con_2 = self.conv_2(con_1) 
        con_2 = self.conv_3(con_2)

        return con_2 #256

class RXDnet(nn.Module):
    def __init__(self, config_model):
        super().__init__()
        
        self.config_model = config_model

        self.yolo_1 = YOLOLayer(self.config_model, layer_no=0, in_ch=2048)
        self.yolo_2 = YOLOLayer(self.config_model, layer_no=1, in_ch=1024)
        self.yolo_3 = YOLOLayer(self.config_model, layer_no=2, in_ch=512)

        self.DFL_1 = RXD(256)
        self.DFL_2 = RXD(512)
        self.DFL_3 = RXD(1024)

        self.conv_0 = nn.Sequential(
                                    nn.Conv2d(3, 64, 3, 1, 1, bias=False),
                                    nn.BatchNorm2d(64),
                                    nn.ReLU(),
                                    nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.conv_1 = nn.Sequential(
                                    nn.Conv2d(64, 128, 3, 1, 1, bias=False),
                                    nn.BatchNorm2d(128),
                                    nn.ReLU(),
                                    nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.conv_2 = nn.Sequential(
                                    nn.Conv2d(128, 256, 3, 1, 1, bias=False),
                                    nn.BatchNorm2d(256),
                                    nn.ReLU(),
                                    nn.MaxPool2d(kernel_size=2, stride=2)
        )    
        self.conv_3 = nn.Sequential(
                                    nn.Conv2d(256, 512, 3, 1, 1, bias=False),
                                    nn.BatchNorm2d(512),
                                    nn.ReLU(),
                                    nn.MaxPool2d(kernel_size=2, stride=2)
        ) 
        self.conv_4 = nn.Sequential(
                                    nn.Conv2d(512, 1024, 3, 1, 1, bias=False),
                                    nn.BatchNorm2d(1024),
                                    nn.ReLU(),
                                    nn.MaxPool2d(kernel_size=2, stride=2)
        ) 
        # self.conv_5 = nn.Sequential(
        #                             nn.Conv2d(512, 1024, 3, 1, 1, bias=False),
        #                             nn.BatchNorm2d(1024),
        #                             nn.ReLU(),
        #                             nn.MaxPool2d(kernel_size=2, stride=2)
        # ) 

    def yolo_process(self, x, labels, num, train):
        if train == False:
            if num == 1:
                x = self.yolo_1(x)
            elif num == 2:
                x = self.yolo_2(x)
            elif num == 3:
                x = self.yolo_3(x)
        else:
            if num == 1:
                x, *losses = self.yolo_1(x, labels)
            elif num == 2:
                x, *losses = self.yolo_2(x, labels)
            elif num == 3:
                x, *losses = self.yolo_3(x, labels)
            for name, loss in zip(["xy", "wh", "obj", "cls"], losses):
                self.loss_dict[name] += loss
        
        return x

    def forward(self, x, x2, labels=None, labels2=None):
        train = labels is not None
        self.loss_dict = defaultdict(float)
        output = []

        x = self.conv_0(x) 
        x2 = self.conv_0(x2) #64, 208, 208

        x = self.conv_1(x) 
        x2 = self.conv_1(x2) #64, 208, 208

        x = self.conv_2(x)
        x2 = self.conv_2(x2) #128, 104, 104

        a = self.DFL_1(x, x2)
        a = self.yolo_process(a, labels, 3, train) #512, 52, 52
        output.append(a)

        x = self.conv_3(x)
        x2 = self.conv_3(x2) #512, 26, 26

        a = self.DFL_2(x, x2)
        a = self.yolo_process(a, labels, 2, train) #512, 26, 26
        output.append(a)

        x = self.conv_4(x)
        x2 = self.conv_4(x2) #1024, 13, 13

        a = self.DFL_3(x, x2)
        a = self.yolo_process(a, labels, 1, train) # 1024, 13, 13
        output.append(a)

        if train:
            return sum(output)
        else:
            return torch.cat(output, dim=1)
