import torch
from torch import nn
import torch.nn.functional as F
import torchvision

# Define the architecture
class Net(nn.Module):
    """
    A simple CNN model

    Args:
        num_classes: An integer indicating the number of classes in the dataset.
    """
    def __init__(self, num_classes=10) -> None:
        super(Net, self).__init__()
        self.backbone = "resnet50"
        self.classifier_layers = []
        self.new_layers = []
        self.pretrained_model = torchvision.models.resnet50(weights=torchvision.models.ResNet50_Weights.IMAGENET1K_V2)
        self.classifier_layers = [self.pretrained_model.fc]
            
        self.pretrained_model.fc = nn.Linear(in_features=2048, out_features=102, bias=True)
        self.new_layers = [self.pretrained_model.fc]
        self.dummy_param = nn.Parameter(torch.empty(0))
        
        # Initialize metrics buffer. element 0 is loss, and element 1 is accuracy.
        self.register_buffer("train_metrics", torch.tensor([float("inf"), 0.0]))
        self.register_buffer("val_metrics", torch.tensor([float("inf"), 0.0]))


    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.pretrained_model(x)