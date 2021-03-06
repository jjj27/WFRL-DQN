import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F

Variable = autograd.Variable


class DQN(nn.Module):
    def __init__(self, hiddenSize = 500):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(6, 256)
        self.fc1.weight.data.normal_(0, 0.1)  # initialization

        self.fc2 = nn.Linear(256, 128)
        self.fc2.weight.data.normal_(0, 0.1)  # initialization

        # self.fc3 = nn.Linear(100, 100)
        # self.fc3.weight.data.normal_(0, 0.1)  # initialization

        # self.fc4 = nn.Linear(100, 100)
        # self.fc4.weight.data.normal_(0, 0.1)  # initialization

        self.out = nn.Linear(128, 5)
        self.out.weight.data.normal_(0, 0.1)  # initialization

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)

        x = self.fc2(x)
        x = F.relu(x)
        # x = self.fc3(x)
        # x = F.relu(x)
        # x = self.fc4(x)
        # x = F.relu(x)

        actions_value = self.out(x)
        return actions_value

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def get_n_params(self):
        pp = 0
        for p in list(self.parameters()):
            nn = 1
            for s in list(p.size()):
                nn = nn * s
            pp += nn
        return pp



#class DQN(nn.Module):
#
#    def __init__(self, hiddenSize = 500):
#
#        super(DQN, self).__init__()
#
#        self.fc1 = nn.Linear(6, hiddenSize)
#        self.fc1.weight.data.normal_(0, 0.1)  # initialization
#        # self.fc2 = nn.Linear(200, 200)
#        # self.fc2.weight.data.normal_(0, 0.1)  # initialization
#        self.out = nn.Linear(hiddenSize, 5)
#        self.out.weight.data.normal_(0, 0.1)  # initialization
#
#        # self.main = nn.Sequential(
#
#
#            # nn.Linear(4, 100),
#            # nn.ReLU(),
#            # nn.Linear(3, 1)
#
#            # nn.Conv2d(4, 32, 8, 4, 0),
#            # nn.ReLU(inplace=True),
#            # nn.Conv2d(32, 64, 4, 2, 0),
#            # nn.ReLU(inplace=True),
#            # nn.Conv2d(64, 64, 3, 1, 0),
#            # nn.ReLU(inplace=True),
#            # nn.Conv2d(64, 512, 7, 4, 0),
#            # nn.ReLU(inplace=True),
#            # nn.Conv2d(512, 3, 1, 1, 0)
#		#)
#    def forward(self, x):
#        x = self.fc1(x)
#        x = F.relu(x)
#        # x = self.fc2(x)
#        # x = F.relu(x)
#        actions_value = self.out(x)
#        return actions_value
#