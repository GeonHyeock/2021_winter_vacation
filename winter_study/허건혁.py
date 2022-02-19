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
path = "/home/inhamath/inhamath/kaggle_FSWJ"


# # 데이터 준비

# ## 데이터 불러오기

def GH_img_load(my_path,my_label=False):
    if bool(my_label):
        data,label,count = [],[],0
        file_list = [img for img in os.listdir(my_path)]
        for file in file_list:
            img_label = my_label[int(file.split(".")[0])]
            file = my_path + "/" + file
            
            img_data = np.array(PIL.Image.open(file))
            if img_data.size == 400 : count += 1; continue
                
            img_data = np.moveaxis(img_data, source = 2,destination = 0)
            data.append(img_data)
            label.append(img_label)
        print("train_data의 채널이 1인 데이터의 갯수 : ", count)
        return {"data" : np.array(data), "label" : label}
    
    data,label,count = [],[],0
    file_list = [my_path + "/" + img for img in os.listdir(my_path)]
    for file in file_list:
        a = np.array(PIL.Image.open(file))
        if a.size == 400:
            count += 1;data.append(np.zeros((3,20,20))); 
            continue
        a = np.moveaxis(a, source = 2,destination = 0)
        data.append(a)
    print("test_data의 채널이 1인 데이터의 갯수 : ", count)
    return np.array(data)

my_label_csv = pd.read_csv(path + "/trainLabels.csv")
label = my_label_csv.Class.unique().tolist()
my_label_csv["label"] = my_label_csv.Class.map(lambda x : label.index(x))

my_label = dict(zip(my_label_csv["ID"],my_label_csv["label"]))

# ## 데이터 셋 만들기
class GH_Dataset_train(data.Dataset): 
    def __init__(self,X,Y):
        self.x_data = torch.from_numpy(X).type(dtype=torch.float32).resize_((len(X),3,20,20))
        self.y_data = torch.tensor(Y).resize_(len(X),1)

    def __len__(self): 
        return len(self.x_data)
    
    def __getitem__(self, idx): 
        x = self.x_data[idx]
        y = self.y_data[idx]
        return x, y

class GH_Dataset_test(data.Dataset):
    def __init__(self,X,Y):
        self.x_data = torch.from_numpy(X).type(dtype=torch.float32).resize_((len(X),3,20,20))
        self.y_data = torch.tensor(Y).resize_(len(X),1)

    def __len__(self): 
        return len(self.x_data)
    
    def __getitem__(self, idx): 
        x = self.x_data[idx]
        y = self.y_data[idx]
        return x, y

batch_size = 32

train_data = GH_img_load(path + "/trainResized/trainResized",my_label) 

train_dataset = GH_Dataset_train(train_data["data"][1000:],train_data["label"][1000:])
train_loader = data.DataLoader(dataset=train_dataset,batch_size=batch_size,shuffle=True)

test_dataset = GH_Dataset_test(train_data["data"][:1000],train_data["label"][:1000])
test_loader = data.DataLoader(dataset=test_dataset,batch_size=batch_size,shuffle=False)


## 모델
class GH(nn.Module):
    def __init__(self):
        super(GH, self).__init__()
        self.l1 = nn.Conv2d(3, 64, 3, padding=1)

        self.l2 = nn.Conv2d(64, 64, 3, padding=1)
        self.l3 = nn.Conv2d(64, 128, 3, padding=1)

        self.l4 = nn.Conv2d(128, 128, 3, padding=1)
        self.l5 = nn.Conv2d(128, 256, 3, padding=1)

        self.l6 = nn.Conv2d(256, 256, 3, padding=1)
        self.l7 = nn.Conv2d(256, 512, 3, padding=1)

        self.l8 = nn.Conv2d(512, 512 , 3, padding=1)
        self.l9 = nn.Conv2d(512, 1024, 3, padding=1)

        self.l10 = nn.Conv2d(1024, 1024, 3, padding=1)
        self.l11 = nn.Conv2d(1024, 1024, 3, padding=1)

        self.ll1 = nn.Linear(4096, 2048)
        self.ll2 = nn.Linear(2048, 512)
        self.ll3 = nn.Linear(512, 62)

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
        x = F.relu(self.l1(x))  #(n,64,32,32)
        residual = x            #residual : (n,64,32,32)

        x, residual = self.GH_Resnet(x, residual, 3, self.l2, self.l3,GH_POOL=False) 
        # (n,128,20,20)
        x, residual = self.GH_Resnet(x, residual, 1, self.l4, self.l5)  
        # (n,256,10,10)
        x, residual = self.GH_Resnet(x, residual, 3, self.l6, self.l7)  
        # (n,512,5,5)
        x, residual = self.GH_Resnet(x, residual, 1, self.l8, self.l9)
        # (n,512,2,2)

        x = x.view(-1, 4096)  #(n,4096)
        x = F.relu(self.ll1(x))  #(n,2048)
        x = F.relu(self.ll2(x))  #(n,512 )
        x = F.relu(self.ll3(x))  #(n,100 )
        return x  #(n,100 )

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
    torch.save(model.state_dict(), path + "/model_param/GH_2" + str(correct)[6:] + '.pt')
    print(f'Test set: Average loss : {test_loss:.4f}, Accuracy : {correct}/{len(test_loader.dataset)}'
          f'({100. * correct / len(test_loader.dataset):.0f}%)')

model = GH()
model.load_state_dict(torch.load(path + "/model_param/GH_2(627).pt"))
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.00001)
# # 모델 학습

if False:
    since = time.time()
    for epoch in range(1,11):
        epoch_start = time.time()
        train(epoch)
        test()
        m, s = divmod(time.time() - epoch_start, 60)
        print(f'Training time: {m:.0f}m {s:.0f}s')
        
    m, s = divmod(time.time() - since, 60)
    print(f'Total time : {m:.0f}m {s: .0f}s \nModel was trained on {device}!')

#모델 제출

class GH_Dataset_submission(data.Dataset):
    def __init__(self,X):
        self.x_data = torch.from_numpy(X).type(dtype=torch.float32).resize_((len(X),3,20,20))

    def __len__(self): 
        return len(self.x_data)
    
    def __getitem__(self, idx): 
        x = self.x_data[idx]
        return x

submission_dict = {label.index(x) : x for x in label}

submission_data = GH_img_load(path + "/testResized/testResized")
submission_dataset = GH_Dataset_submission(submission_data)
submission_loader = data.DataLoader(dataset=submission_dataset,batch_size=batch_size)

result = []
for data in submission_loader:
    output = model(data.to(device))
    pred = output.data.max(1, keepdim=True)[1]
    result += list(map(lambda x : submission_dict[int(x)],pred))
submission = pd.read_csv(path + "/sampleSubmission.csv")
submission["Class"] = result
submission.to_csv("my_submission.csv", index=False)
