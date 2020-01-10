import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import torch.utils.data
from torch.optim.lr_scheduler import StepLR
import numpy as np
import matplotlib.pyplot as plt
import os


# LeNet model that is under attack
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout2d(0.5)
        self.fc1 = nn.Linear(2000, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output

def get_loaders(batch_size):
    kwargs = {'num_workers': 1, 'pin_memory': True}

    transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3801,))
            ])
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            'data', train=True, download=True,
            transform=transform
        ),
        batch_size=batch_size, shuffle=True, **kwargs
    )

    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            'data', train=False,
            transform=transform
        ),
        batch_size=batch_size, shuffle=True, **kwargs
    )
    return train_loader, test_loader


def train_and_save(batch_size, lr, epochs, log_interval, model_save_file_name):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    train_loader, test_loader = get_loaders(batch_size)

    model = Net().to(device)
    optimizer = optim.Adadelta(model.parameters(), lr=lr)
    scheduler = StepLR(optimizer, step_size=1, gamma=0.7)
    for epoch in range(epochs):
        # train
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()
            if batch_idx % log_interval == 0:
                print 'Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx*len(data), len(train_loader.dataset),
                    100.*batch_idx/len(train_loader), loss.item()
                )
        # test
        model.eval()
        test_loss = 0
        correct = 0
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                test_loss += F.nll_loss(output, target, reduction='sum').item()
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()

        test_loss /= len(test_loader.dataset)
        print '\n Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
            test_loss, correct, len(test_loader.dataset),
            100.*correct/len(test_loader.dataset)
        )

        # step
        scheduler.step()

    torch.save(model.state_dict(), model_save_file_name)

def fgsm_attack(data, eps, data_grad):
    sign_data_grad = data_grad.sign()
    perturbed_data = data + eps*sign_data_grad
    return perturbed_data

def add_example(perturbed_data, init_pred, final_pred, adv_examples):
    adv_ex = perturbed_data.squeeze().detach().cpu().numpy()
    adv_examples.append(
        (
            init_pred.item(), final_pred.item(), adv_ex
        )
    )

def test_attack(model, device, test_loader, eps):
    correct = 0
    adv_examples = []
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        data.requires_grad = True
        output = model(data)
        init_pred = output.max(1, keepdim=True)[1]

        if init_pred.item() != target.item():
            continue
        loss = F.nll_loss(output, target)
        model.zero_grad()

        loss.backward()
        data_grad = data.grad.data

        perturbed_data = fgsm_attack(data, eps, data_grad)
        output = model(perturbed_data)
        final_pred = output.max(1, keepdim=True)[1]
        # final_pred = init_pred
        if final_pred.item() == target.item():
            correct += 1
            if eps == 0 and len(adv_examples) < 5:
                add_example(perturbed_data, init_pred, final_pred, adv_examples)
        elif len(adv_examples) < 5:
                add_example(perturbed_data, init_pred, final_pred, adv_examples)

    final_acc = correct / float(len(test_loader))
    print 'Epsilon: {}\tTest Accuracy = {}/{} = {}'.format(
        eps, correct, len(test_loader), final_acc
    )

    return final_acc, adv_examples

def attack_net(model_save_file_name):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = Net().to(device)
    model.load_state_dict(torch.load(model_save_file_name, map_location='cpu'))

    model.eval()
    epsilons = [0, .05, .1, .15, .2, .25, .3]
    accuracies = []
    examples = []
    _, test_loader = get_loaders(1)

    for eps in epsilons:
        acc, ex = test_attack(model, device, test_loader, eps)
        accuracies.append(acc)
        examples.append(ex)

    plt.figure(figsize=(5,5))
    plt.plot(epsilons, accuracies, "*-")
    plt.yticks(np.arange(0, 1.1, step=0.1))
    plt.xticks(np.arange(0, .35, step=0.05))
    plt.title("Accuracy vs Epsilon")
    plt.xlabel("Epsilon")
    plt.ylabel("Accuracy")
    plt.show()

    count = 0
    plt.figure(figsize=(8, 10))
    for i in range(len(epsilons)):
        for j in range(len(examples[i])):
            count += 1
            plt.subplot(len(epsilons), len(examples[0]), count)
            plt.xticks([], [])
            plt.yticks([], [])
            if j == 0:
                plt.ylabel('Eps: {}'.format(epsilons[i]), fontsize=14)
            orig, adv, ex = examples[i][j]
            plt.title('{}->{}'.format(orig, adv))
            plt.imshow(ex, cmap='gray')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    batch_size = 4
    lr = 1.
    epochs = 2
    log_interval = 100
    model_save_file_name = 'mnist_cnn.pt'
    if not os.path.exists(model_save_file_name):
        train_and_save(batch_size, lr, epochs, log_interval, model_save_file_name)
    attack_net(model_save_file_name)