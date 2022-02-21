#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import PIL
import os
import time
import torch
import torch.nn.functional as F
import pickle

from torch import nn, optim, cuda
from torch.utils import data
from torchvision import datasets, transforms
from GH_model import GH
from GH_data_processing import GH_Dataset

device = 'cuda' if cuda.is_available() else 'cpu'
path = "/home/inhamath/inhamath/Dacon/model_param"

with open("/home/inhamath/inhamath/Dacon/train_loader.pickle", 'rb') as f:
    train_loader = pickle.load(f)
    
with open('/home/inhamath/inhamath/Dacon/test_loader.pickle', 'rb') as f:
    test_loader = pickle.load(f)    


# # 모델 정의

# In[9]:


from GH_model import GH

model = GH()
model.to(device)
if True:
    model.load_state_dict(torch.load(path + "/GH(5850).pt"))



criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.00001)

def train(epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, torch.squeeze(target))
        loss.backward()
        optimizer.step()
        if batch_idx % 100000 == 0:
            print('==================\nTrain Epoch : {} | Loss : {:.6f}'.format(epoch, loss.item()))

def test():
    model.eval()
    test_loss = 0
    correct = 0
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        test_loss += criterion(output, torch.squeeze(target)).item()
        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()
    test_loss /= len(test_loader.dataset)
    torch.save(model.state_dict(), path + "/GH" + str(correct)[6:] + '.pt')
    print(f'Test set: Average loss : {test_loss:.4f}, Accuracy : {correct}/{len(test_loader.dataset)}'
          f'({100. * correct / len(test_loader.dataset):.0f}%)') 


# # 모델 학습

# In[10]:


since = time.time()
for epoch in range(1,6):
    epoch_start = time.time()
    train(epoch)
    test()
    m, s = divmod(time.time() - epoch_start, 60)
    print(f'Training time: {m:.0f}m {s:.0f}s')
    
m, s = divmod(time.time() - since, 60)
print(f'Total time : {m:.0f}m {s: .0f}s \nModel was trained on {device}!')