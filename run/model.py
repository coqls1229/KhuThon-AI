import torch
import torch.nn as nn

class FertilizerClassifier(nn.Module):
    def __init__(self, input_size=9, hidden_size=32, num_classes=4):  # <-- 수정
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_classes)
        )

    def forward(self, x):
        return self.net(x)
