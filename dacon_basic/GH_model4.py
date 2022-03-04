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
        self.l1 = nn.Conv2d(3, 32, 3, padding=1)

        self.l2 = nn.Conv2d(32, 32, 3, padding=1)
        self.l3 = nn.Conv2d(32, 64, 3, padding=1)

        self.l4 = nn.Conv2d(64, 64, 3, padding=1)
        self.l5 = nn.Conv2d(64, 128, 3, padding=1)

        self.l6 = nn.Conv2d(128, 128, 3, padding=1)
        self.l7 = nn.Conv2d(128, 256, 3, padding=1)

        self.l8 = nn.Conv2d(256, 256 , 3, padding=1)
        self.l9 = nn.Conv2d(256, 512, 3, padding=1)

        self.l10 = nn.Conv2d(512, 512, 3, padding=1)
        self.l11 = nn.Conv2d(512, 512, 3, padding=1)

        self.ll1 = nn.Linear(2048, 1024)
        self.ll2 = nn.Linear(1024, 512)
        self.ll3 = nn.Linear(512, 10)

        self.dropout = nn.Dropout(0.5)

    def GH_Resnet(self, x, residual, k, GH_CONV, GH_CONV2, GH_POOL=True):
        for i in range(k):
            x = F.relu(GH_CONV(x))
            x = GH_CONV(x)
            x += residual
            residual = x

        x = F.relu(GH_CONV2(x))
        if GH_POOL:
            x = F.max_pool2d(x, 2)
        residual = x
        return x, residual

    def forward(self, x):       #(n,3,32,32)
        x = F.relu(self.l1(x))  #(n,32,32,32)
        residual = x            #residual : (n,32,32,32)

        x, residual = self.GH_Resnet(x, residual, 3, self.l2, self.l3,GH_POOL=False) 
        # (n,64,32,32)
        x, residual = self.GH_Resnet(x, residual, 3, self.l4, self.l5)  
        # (n,128,16,16)
        x, residual = self.GH_Resnet(x, residual, 3, self.l6, self.l7)  
        # (n,256,8,8)
        x, residual = self.GH_Resnet(x, residual, 2, self.l8, self.l9)
        # (n,512,4,4)
        x, residual = self.GH_Resnet(x, residual, 2, self.l10, self.l11)
        # (n,512,2,2)

        x = x.view(-1, 2048)  #(n,2048)
        x = self.dropout(x)
        x = F.relu(self.ll1(x))  #(n,1024)
        x = self.dropout(x)

        x = F.relu(self.ll2(x))  #(n,512)
        x = self.dropout(x)

        x = F.relu(self.ll3(x))  #(n,10)
        return x  #(n,10)


# In[ ]:




