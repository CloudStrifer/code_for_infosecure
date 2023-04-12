import torch
from torchvision import transforms
from torchvision import datasets
from torch.utils.data import  DataLoader
import torch.nn.functional as F #使用functional中的ReLu激活函数
import torch.optim as optim
import time

#数据的准备
batch_size = 64
#神经网络希望输入的数值较小，最好在0-1之间，所以需要先将原始图像(0-255的灰度值)转化为图像张量（值为0-1）
#仅有灰度值->单通道   RGB -> 三通道 读入的图像张量一般为W*H*C (宽、高、通道数) 在pytorch中要转化为C*W*H
transform = transforms.Compose([
    #将数据转化为图像张量
    transforms.ToTensor(),
    #进行归一化处理，切换到0-1分布 （均值， 标准差）
    transforms.Normalize((0.1307, ), (0.3081, ))
])

train_dataset = datasets.MNIST(root='../datasets/mnist/',
                               train=True,
                               download=True,
                               transform=transform
                               )
train_loader = DataLoader(train_dataset,
                          shuffle=True,
                          batch_size=batch_size
                          )
test_dataset = datasets.MNIST(root='../datasets/mnist/',
                               train=False,
                               download=True,
                               transform=transform
                               )
test_loader = DataLoader(test_dataset,
                          shuffle=False,
                          batch_size=batch_size
                          )


#CNN模型
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        #两个卷积层
        self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=5)  #1为in_channels 10为out_channels
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5)
        #池化层
        self.pooling = torch.nn.MaxPool2d(2)  #2为分组大小2*2
        #全连接层 320 = 20 * 4 * 4
        self.fc = torch.nn.Linear(320, 10)

    def forward(self, x):
        #先从x数据维度中得到batch_size
        batch_size = x.size(0)
        #卷积层->池化层->激活函数
        x = F.relu(self.pooling(self.conv1(x)))
        x = F.relu(self.pooling(self.conv2(x)))
        x = x.view(batch_size, -1)  #将数据展开，为输入全连接层做准备
        x = self.fc(x)
        return x
model = Net()
#在这里加入两行代码，将数据送入GPU中计算！！！
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)  #将模型的所有内容放入cuda中


#设置损失函数和优化器
criterion = torch.nn.CrossEntropyLoss()
#神经网络已经逐渐变大，需要设置冲量momentum=0.5
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

#训练
#将一次迭代封装入函数中
def train(epoch):
    running_loss = 0.0
    for batch_idx, data in enumerate(train_loader, 0):   #在这里data返回输入:inputs、输出target
        inputs, target = data
        #在这里加入一行代码，将数据送入GPU中计算！！！
        inputs, target = inputs.to(device), target.to(device)

        optimizer.zero_grad()

        #前向 + 反向 + 更新
        outputs = model(inputs)
        loss = criterion(outputs, target)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if batch_idx % 300 == 299:
            print('[%d, %5d] loss: %.3f' % (epoch + 1, batch_idx + 1, running_loss / 300))

def test():
    correct = 0
    total = 0
    with torch.no_grad():  #不需要计算梯度
        for data in test_loader:   #遍历数据集中的每一个batch
            images, labels = data  #保存测试的输入和输出
            #在这里加入一行代码将数据送入GPU
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)#得到预测输出
            _, predicted = torch.max(outputs.data, dim=1)#dim=1沿着索引为1的维度(行)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print('Accuracy on test set:%d %%' % (100 * correct / total))

if __name__ == '__main__':
    localtime = time.localtime(int(time.time()))
    # 利用strftime()函数重新格式化时间
    dt = time.strftime('%Y:%m:%d %H:%M:%S', localtime)
    print(dt)  # 返回当前时间：2021:09:09 19:17:29

    for epoch in range(10):
        train(epoch)
        test()
    localtime2 = time.localtime(int(time.time()))
    # 利用strftime()函数重新格式化时间
    dt2 = time.strftime('%Y:%m:%d %H:%M:%S', localtime2)
    print(dt2)
