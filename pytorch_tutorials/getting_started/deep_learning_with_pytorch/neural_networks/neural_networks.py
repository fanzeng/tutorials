import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 3)
        self.conv2 = nn.Conv2d(6, 16, 3)
        self.fc1 = nn.Linear(16*6*6, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]
        print 'x.size() =', x.size()
        num_features = 1
        for s in size:
            num_features *= s
        print 'num_features =', num_features
        return num_features

net = Net()
print net
params = list(net.parameters())
print 'len(params) =', len(params)
for i in range(len(params)):
    print 'params[{:d}].size() ='.format(i), params[i].size()

input = torch.randn(1, 1, 32, 32)
print 'input =', input
out = net(input)
print 'out.shape =', out.shape

net.zero_grad()
out.backward(torch.randn(1, 10))

output = net(input)
target = torch.rand(10)
target = target.view(1, -1)
criterion = nn.MSELoss()

loss = criterion(output, target)
print loss

print 'loss.grad_fn =', loss.grad_fn
print 'loss.grad_fn.next_functions[0][0] =', loss.grad_fn.next_functions[0][0]
print 'loss.grad_fn.next_functions[0][0].next_functions[0][0] =', loss.grad_fn.next_functions[0][0].next_functions[0][0]

net.zero_grad()

print 'conv1.bias.grad before backward'
print net.conv1.bias.grad

loss.backward()

print 'conv1.bias.grad after backward'
print net.conv1.bias.grad

learning_rate = 0.01
# for f in net.parameters():
#     f.data.sub_(f.grad.data*learning_rate)

print 'net.parameters() =', net.parameters
optimizer = optim.SGD(net.parameters(), lr=0.01)

optimizer.zero_grad()
output = net(input)
loss = criterion(output, target)
loss.backward()
optimizer.step()