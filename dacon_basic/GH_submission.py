#!/usr/bin/env python
# coding: utf-8

# In[10]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import PIL
import os
import time
import torch
import torch.nn.functional as F
import pickle

from GH_model import GH
from torch import nn, optim, cuda
from torch.utils import data
from torchvision import datasets, transforms

device = 'cuda' if cuda.is_available() else 'cpu'
path = "/home/inhamath/inhamath/Dacon/test"

with open("/home/inhamath/inhamath/Dacon/label_data_dict.pickle", 'rb') as f:
    label_data_dict = pickle.load(f)    
label_data_dict ={b:a for a,b in label_data_dict.items()}

model = GH()
model.load_state_dict(torch.load("Dacon/model_param/" + "GH(5850).pt"))
model.to(device)

# In[11]:


class GH_Dataset_submission(data.Dataset):
    def __init__(self,X):
        self.x_data = torch.from_numpy(X).type(dtype=torch.float32).resize_((len(X),3,32,32))

    def __len__(self): 
        return len(self.x_data)
    
    def __getitem__(self, idx): 
        x = self.x_data[idx]
        return x


# In[14]:


submission_img = []

datas = sorted(os.listdir(path))
for data in datas:
    data_img  = np.array(PIL.Image.open(f"{path}/{data}"))
    data_img  = np.moveaxis(data_img, source = 2,destination = 0)
    submission_img.append(data_img)
submission_dataset = GH_Dataset_submission(np.array(submission_img))
submission_loader = torch.utils.data.DataLoader(dataset=submission_dataset)

result = []
for data in submission_loader:
    output = model(data.to(device))
    pred = output.data.max(1, keepdim=True)[1]
    result += list(map(lambda x : label_data_dict[int(x)],pred))
submission = pd.read_csv("/home/inhamath/inhamath/Dacon/sample_submission.csv")
submission["target"] = result
submission.to_csv("/home/inhamath/inhamath/Dacon/GH_submission.csv", index=False)