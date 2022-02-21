
# # 라이브러리
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
path = "/home/inhamath/inhamath/Dacon/train"


# # 데이터 준비

# ## 데이터 불러오기
# 
# data_img2 : 좌우반전  
# data_img3 : 상하반전  
# data_img4 : 상하,좌우반전

labels = os.listdir(path)
if ".DS_Store" in labels: labels.remove(".DS_Store")
label_data_dict = dict(zip(labels,range(len(labels))))

train_img,train_label = [],[]

for label in labels:
    data_list = os.listdir(f"{path}/{label}")
    if ".DS_Store" in data_list: data_list.remove(".DS_Store")

    for data in data_list:
        data_img  = np.array(PIL.Image.open(f"{path}/{label}/{data}"))
        data_img  = np.moveaxis(data_img, source = 2,destination = 0)
        train_img.append(data_img)
        
        # 좌우 반전
        data_img2 = data_img[:,:,::-1]
        train_img.append(data_img2)
        
        #상하 반전
        data_img3 = data_img[:,::-1,:]
        train_img.append(data_img3)
        
        #좌우,상하 반전
        data_img4 = data_img[:,::-1,::-1]
        train_img.append(data_img4)
        
        train_label += [label_data_dict[label]] * 4
    
train_data_dict = {"train_img" : np.array(train_img), "train_label" : np.array(train_label)}

# ## 데이터 셋 만들기
class GH_Dataset(torch.utils.data.Dataset): 
    def __init__(self,X,Y):
        self.x_data = torch.from_numpy(X).type(dtype=torch.float32)
        self.y_data = torch.tensor(Y).resize_(len(X),1)

    def __len__(self): 
        return len(self.x_data)
    
    def __getitem__(self, idx): 
        x = self.x_data[idx]
        y = self.y_data[idx]
        return x, y


batch_size = 512

dataset = GH_Dataset(train_data_dict["train_img"],train_data_dict["train_label"])
train_dataset,test_dataset = torch.utils.data.random_split(dataset,[190000,10000])

train_loader = torch.utils.data.DataLoader(dataset=train_dataset,batch_size=batch_size)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset,batch_size=batch_size)


# 데이터 저장
import pickle

with open('/home/inhamath/inhamath/Dacon/train_loader.pickle', 'wb') as f:
    pickle.dump(train_loader, f)
with open('/home/inhamath/inhamath/Dacon/test_loader.pickle', 'wb') as f:
    pickle.dump(test_loader, f)
with open('/home/inhamath/inhamath/Dacon/label_data_dict.pickle', 'wb') as f:
    pickle.dump(label_data_dict, f)


