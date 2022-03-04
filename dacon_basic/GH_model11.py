#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import PIL
import os

import torch
import torch.nn.functional as F
from torch import nn, optim, cuda
from torch.utils import data
from torchvision import datasets, transforms
import time

device = 'cuda' if cuda.is_available() else 'cpu'


# In[3]:


class GH(nn.Module):
    def __init__(self):
        super(GH, self).__init__()
        self.l1 = nn.Conv2d(3, 3, 3, padding=1, bias = False)
        self.l1_1 = nn.Conv2d(3,32,3, padding=1, bias = False)

        self.l2 = nn.Conv2d(32, 32, 3, padding=1, bias = False)
        self.l3 = nn.Conv2d(32, 64, 3, padding=1, bias = False)

        self.l4 = nn.Conv2d(64, 64, 3, padding=1, bias = False)
        self.l5 = nn.Conv2d(64, 128, 3, padding=1, bias = False)

        self.l6 = nn.Conv2d(128, 128, 3, padding=1, bias = False)
        self.l7 = nn.Conv2d(128, 256, 3, padding=1, bias = False)

        self.l8 = nn.Conv2d(256, 256 , 3, padding=1, bias = False)
        self.l9 = nn.Conv2d(256, 512, 3, padding=1, bias = False)

        self.l10 = nn.Conv2d(512, 512, 3, padding=1, bias = False)
        self.l11 = nn.Conv2d(512, 1024, 3, padding=1, bias = False)

        self.l12 = nn.Conv2d(1024, 1024, 3, padding=1, bias = False)

        self.ll1 = nn.Linear(4096, 2048)
        self.ll2 = nn.Linear(2048, 512)
        self.ll3 = nn.Linear(512, 10)

        self.bn1 = nn.BatchNorm2d(3)
        self.bn2 = nn.BatchNorm2d(1024)

        self.dropout = nn.Dropout(0.5)

        self.active = nn.LeakyReLU()

    def GH_Resnet(self, x, residual, k, GH_CONV, GH_CONV2, GH_POOL=True):
        for i in range(k):
            x = self.active(GH_CONV(x))
            x = self.active(GH_CONV(x))
            x += residual
            residual = x
        x = self.active(GH_CONV2(x))

        if GH_POOL:
            x = F.max_pool2d(x, 2)
        residual = x
        return x, residual

    def forward(self, x):
        x = self.bn1(x)
        residual = x
        
        # (n,3,32,32)
        x, residual = self.GH_Resnet(x, residual, 3, self.l1, self.l1_1, GH_POOL=False) 
        # (n,32,32,32)
        x, residual = self.GH_Resnet(x, residual, 3, self.l2, self.l3, GH_POOL=False) 
        # (n,64,32,32)
        x, residual = self.GH_Resnet(x, residual, 3, self.l4, self.l5, GH_POOL=False)
        # (n,128,32,32)
        x, residual = self.GH_Resnet(x, residual, 3, self.l6, self.l7)  
        # (n,256,16,16)
        x, residual = self.GH_Resnet(x, residual, 3, self.l8, self.l9)
        # (n,512,8,8)
        x, residual = self.GH_Resnet(x, residual, 3, self.l10, self.l11)
        # (n,1024,4,4)
        x, residual = self.GH_Resnet(x, residual, 3, self.l12, self.l12)

        x = self.bn2(x)
        x = x.view(-1, 4096)  #(n,4096)
        x = self.dropout(x)
        x = F.relu(self.ll1(x))  #(n,1024)
        x = self.dropout(x)
        x = F.relu(self.ll2(x))  #(n,256)
        x = self.dropout(x)

        x = F.relu(self.ll3(x))  #(n,10)
        return x  #(n,10)


# In[ ]:




