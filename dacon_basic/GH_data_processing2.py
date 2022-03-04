
# # 라이브러리
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import PIL
import torch
import torch.nn.functional as F
import time
import random

from torch import nn, optim, cuda
from torch.utils import data
from torchvision import datasets, transforms


device = 'cuda' if cuda.is_available() else 'cpu'
path = "/home/inhamath/inhamath/Dacon/train"


# # 데이터 준비

# ## 데이터 불러오기
# 
# data_img2 : 좌우반전  


labels = os.listdir(path)
if ".DS_Store" in labels: labels.remove(".DS_Store")
label_data_dict = dict(zip(labels,range(len(labels))))

train_img,train_label = [],[]
test_img,test_label = [],[]

for label in labels:
    data_list = os.listdir(f"{path}/{label}")
    if ".DS_Store" in data_list: data_list.remove(".DS_Store")

    for data in data_list[:4500]:
        data_img = PIL.Image.open(f"{path}/{label}/{data}")
        
        data_img1  = np.array(data_img)
        data_img1  = np.moveaxis(data_img1, source = 2,destination = 0)
        train_img.append(data_img1)
        
        # 좌우 반전
        data_img2 = data_img1[:,:,::-1]
        train_img.append(data_img2)
        
        # 회전
        rotate_img = data_img.rotate(random.randint(-60, 60))
        rotate_img = np.array(rotate_img)
        rotate_img = np.moveaxis(rotate_img, source = 2,destination = 0)
        train_img.append(rotate_img)
        
        
        
        train_label += [label_data_dict[label]] * 3
        
    for data in data_list[4500:]:
        data_img = PIL.Image.open(f"{path}/{label}/{data}")
        
        data_img1  = np.array(data_img)
        data_img1  = np.moveaxis(data_img1, source = 2,destination = 0)
        test_img.append(data_img1)
        
        # 좌우 반전
        data_img2 = data_img1[:,:,::-1]
        test_img.append(data_img2)
        
        # 회전
        rotate_img = data_img.rotate(random.randint(-60, 60))
        rotate_img = np.array(rotate_img)
        rotate_img = np.moveaxis(rotate_img, source = 2,destination = 0)
        test_img.append(rotate_img)
        
        test_label += [label_data_dict[label]] * 3
    
train_data_dict = {"train_img" : np.array(train_img), "train_label" : np.array(train_label)}
test_data_dict = {"test_img" : np.array(test_img), "test_label" : np.array(test_label)}

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


batch_size = 256


train_dataset = GH_Dataset(train_data_dict["train_img"],train_data_dict["train_label"])
test_dataset = GH_Dataset(test_data_dict["test_img"],test_data_dict["test_label"])

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


