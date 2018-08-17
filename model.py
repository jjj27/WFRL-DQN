import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F

Variable = autograd.Variable

class DQN(nn.Module):

    def __init__(self):

        super(DQN, self).__init__()

        self.fc1 = nn.Linear(4, 1000)
        self.fc1.weight.data.normal_(0, 0.1)  # initialization
        # self.fc2 = nn.Linear(200, 200)
        # self.fc2.weight.data.normal_(0, 0.1)  # initialization
        self.out = nn.Linear(1000, 3)
        self.out.weight.data.normal_(0, 0.1)  # initialization

        # self.main = nn.Sequential(


            # nn.Linear(4, 100),
            # nn.ReLU(),
            # nn.Linear(3, 1)

            # nn.Conv2d(4, 32, 8, 4, 0),
            # nn.ReLU(inplace=True),
            # nn.Conv2d(32, 64, 4, 2, 0),
            # nn.ReLU(inplace=True),
            # nn.Conv2d(64, 64, 3, 1, 0),
            # nn.ReLU(inplace=True),
            # nn.Conv2d(64, 512, 7, 4, 0),
            # nn.ReLU(inplace=True),
            # nn.Conv2d(512, 3, 1, 1, 0)
		#)
    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        # x = self.fc2(x)
        # x = F.relu(x)
        actions_value = self.out(x)
        return actions_value
