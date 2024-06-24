import argparse
import warnings
from collections import OrderedDict
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from typing import Dict
from flwr.common import NDArrays, Scalar
from tqdm import tqdm
import numpy as np
from torchvision import datasets, transforms
import os

# #############################################################################
# 1. Regular PyTorch pipeline: nn.Module, train, test, and DataLoader
# #############################################################################

warnings.filterwarnings("ignore", category=UserWarning)
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def get_parameters(net):
    return [val.cpu().numpy() for _, val in net.state_dict().items()]


def set_parameters(net, parameters):
    params_dict = zip(net.state_dict().keys(), parameters)
    state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
    net.load_state_dict(state_dict, strict=True)
    
class Net(nn.Module):
    """Model (simple CNN adapted from 'PyTorch: A 60 Minute Blitz')"""

    def __init__(self) -> None:
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 61 * 61, 400)  # Adjusted input size
        self.fc2 = nn.Linear(400, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))  # Added this line to pass through fc2
        return self.fc3(x)


def train(net, trainloader, valloader, epochs, device=DEVICE):
    """Train the model on the training set."""
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.0001)
    net.train()
    for _ in range(epochs):
        print(f"EPOCH {_+1}/{epochs}")
        for input, labels in trainloader:
            image = input.to(DEVICE)
            label = labels.to(DEVICE)
            optimizer.zero_grad()
            loss = criterion(net(image), label)
            loss.backward()
            optimizer.step()
           
        print("Epoch completed")
    train_loss, train_acc = test(net, trainloader)
    val_loss, val_acc = test(net, valloader)

    results = {
        "train_loss": train_loss,
        "train_accuracy": train_acc,
        "val_loss": val_loss,
        "val_accuracy": val_acc,
    }
    return results


def test(net, testloader):
    """Validate the model on the test set."""
    net.to(DEVICE)
    criterion = torch.nn.CrossEntropyLoss()
    correct, total, loss = 0, 0, 0.0
    with torch.no_grad():
        for images, labels in tqdm(testloader):
            images = images.to(DEVICE)
            labels = labels.to(DEVICE)
            outputs = net(images)
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            loss += criterion(outputs, labels).item()
    return loss, correct / len(testloader.dataset)


def load_data(partition_id):
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize((256,256)),
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ]),
        'val': transforms.Compose([
            transforms.Resize((256,256)),
            transforms.ToTensor(),
        ]),
        'test': transforms.Compose([
        transforms.Resize((256,256)),
            transforms.ToTensor(),
        ]),
    }


    data_dir = "../data"  # Set the directory for the data
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                            data_transforms[x])
                    for x in [ 'test', 'train', 'val']}
    dataloaders = {x: DataLoader(image_datasets[x], batch_size=16,
                                                shuffle=True, num_workers=2)
                for x in ['train', 'val','test']}
    dataset_sizes = {x: len(image_datasets[x]) for x in ['test', 'train', 'val']}
    class_names = image_datasets['train'].classes
    global num_classes
    num_classes= len(class_names)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    # trainloader, testloader1= train_test_split(dataloaders['train'], test_size=0.6, random_state=partition_id)
    trainloader = dataloaders['train']
    testloader = dataloaders['test']
    valloader = dataloaders['val']
    return trainloader, testloader, valloader


# #############################################################################
# 2. Federation of the pipeline with Flower
# #############################################################################

# Get partition id
parser = argparse.ArgumentParser(description="Flower")
parser.add_argument(
    "--partition-id",
    choices=[0, 1, 2],
    default=0,
    type=int,
    help="Partition of the dataset divided into 3 iid partitions created artificially.",
)
partition_id = parser.parse_known_args()[0].partition_id

# Load model and data (simple CNN, CIFAR-10)
net = Net().to(DEVICE)
trainloader, testloader,valloder = load_data(partition_id)


# Define Flower client



# Flower ClientApp



# Legacy mode
if __name__ == "__main__":
    trainloader, testloader, valloader = load_data(partition_id)
    net = Net().to(DEVICE)
    result=train(net, trainloader, valloader, epochs=10)
    test_loss, test_acc = test(net, testloader)
    print(f"Test Loss: {test_loss}, Test Accuracy: {test_acc}")
    print(result)
    