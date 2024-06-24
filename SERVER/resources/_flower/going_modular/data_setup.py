"""
Contains functionality for creating PyTorch DataLoaders for image classification data.
"""
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split, SubsetRandomSampler

from .common import *

NUM_WORKERS = os.cpu_count()

# Normalization values for the different datasets



def split_trainloader(trainloader, percentage, seed=42):
    np.random.seed(seed)
    dataset_size = len(trainloader.dataset)
    indices = list(range(dataset_size))
    split = int(np.floor(percentage * dataset_size))
    np.random.shuffle(indices)

    train_indices, val_indices = indices[split:], indices[:split]

    train_sampler = SubsetRandomSampler(train_indices)
    val_sampler = SubsetRandomSampler(val_indices)

    trainloader_split = DataLoader(trainloader.dataset, batch_size=trainloader.batch_size, sampler=train_sampler, num_workers=trainloader.num_workers)
    valloader_split = DataLoader(trainloader.dataset, batch_size=trainloader.batch_size, sampler=val_sampler, num_workers=trainloader.num_workers)

    return trainloader_split


# Define model, architecture and dataset
# The DataLoaders downloads the training and test data that are then normalized.
def load_datasets(num_clients: int, batch_size: int, resize: int, seed: int, num_workers: int, splitter=10,
                  dataset="cifar", data_path="./data/", data_path_val=""):
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize((299,256)),
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
    
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
                  for x in ['train', 'val', 'test']}

    # Create dataloaders
    dataloaders = {x: DataLoader(image_datasets[x], batch_size=16, shuffle=True, num_workers=0)
               for x in ['train', 'val', 'test']}

    # Get dataset sizes
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val', 'test']}

    class_names = image_datasets['train'].classes
    global num_classes
    num_classes= len(class_names)
  
    
    # trainloader, testloader1= train_test_split(dataloaders['train'], test_size=0.6, random_state=partition_id)
    trainloaders = dataloaders['train']
    testloader = dataloaders['test']
    valloaders = dataloaders['val']
    return trainloaders, valloaders, testloader
