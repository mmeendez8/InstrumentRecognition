import time

import sys
sys.path.append('../src');
sys.path.append('../src/parser');
import os
import nn
from trainNN import trainNN
os.chdir('../')


folder = '11Instruments'
numHarmonics = 10;
percent_Val = 10;
numHidden = [5, 10];
batch_size = [20, 50];
times = 50;
epoch = 500;
alphas = [1, 10, 50];
costs = ["CE"];
lambs = [0, 2];
show = False
k = 5;

trainNN(folder, numHarmonics, percent_Val, numHidden, batch_size, times, epoch, alphas, costs, lambs, k, False);
