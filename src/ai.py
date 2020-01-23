import os
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable


class Network(nn.Module):

    # nb_action - output_size
    def __init__(self, input_size, nb_action):
        super().__init__()
        self.input_size = input_size
        self.nb_action = nb_action

        # Full connections
        self.fc1 = nn.Linear(input_size, 30)  # connect input values with first hidden layer inputs sized of 30
        self.fc2 = nn.Linear(30, nb_action)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        q_values = self.fc2(x)
        return q_values


# Experience replay

class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def size(self):
        return len(self.memory)

    def push(self, event):
        self.memory.append(event)

        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        samples = zip(*random.sample(self.memory, batch_size))
        return map(lambda x: Variable(torch.cat(x, 0)), samples)


class Dqn:
    def __init__(self, input_size, nb_action, gamma):
        self.gamma = gamma
        self.reward_window = []
        self.model = Network(input_size, nb_action)
        self.memory = ReplayMemory(100000)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.last_state = torch.Tensor(input_size).unsqueeze(0)
        self.last_action = 0
        self.last_reward = 0

    def select_action(self, input_state):
        q_values = self.model(Variable(input_state, volatile=True))
        probs = F.softmax(q_values * 7)  # temperature
        return probs.multinomial().data[0, 0]

    def learn(self, batch_state, batch_next_state, batch_reward, batch_action):
        outputs = self.model(batch_state) \
            .gather(1, batch_action.unsqueeze(1)) \
            .squeeze(1)
        next_outputs = self.model(batch_next_state) \
            .detach() \
            .max(1)[0]
        target = self.gamma * next_outputs + batch_reward
        td_loss = F.smooth_l1_loss(outputs, target)
        self.optimizer.zero_grad()
        td_loss.backward(retain_variables=True)
        self.optimizer.step()

    def update(self, reward, new_signal):
        new_state = torch.Tensor(new_signal) \
            .float() \
            .unsqueeze(0)
        self.memory.push((
            self.last_state,
            new_state,
            torch.LongTensor([int(self.last_action)]),
            torch.Tensor([self.last_reward])
        ))
        action = self.select_action(new_state)
        if self.memory.size() > 100:
            batch_state, batch_next_state, batch_reward, batch_action = self.memory.sample(100)
            self.learn(batch_state, batch_next_state, batch_reward, batch_action)
        self.last_action = action
        self.last_state = new_state
        self.last_reward = reward
        self.reward_window.append(reward)
        if len(self.reward_window) > 1000:
            del self.reward_window[0]
        return action

    def score(self):
        # + 1 for zero division protection
        return sum(self.reward_window) / (len(self.reward_window) + 1)

    def save(self):
        torch.save(
            {
                'state_dict': self.model.state_dict(),
                'self_optimizer': self.optimizer.state_dict()
            },
            'last_brain.pth'
        )

    def load(self):
        if os.path.isfile('last_brain.pth'):
            print("=> loading checkpoint... ")
            checkpoint = torch.load('last_brain.pth')
            self.model.load_state_dict(checkpoint['state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
            print("done !")
        else:
            print("no checkpoint found...")
