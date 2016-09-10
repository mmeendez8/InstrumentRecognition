import time

import sys
sys.path.append('../src');
sys.path.append('../src/parser');
import os
import nn
from trainNN import trainNN
os.chdir('../')


folder = '2Instruments'
numHarmonics = 10;
percent_Val = 10;
numHidden = [2, 8, 10];
batch_size = [20];
times = 50;
epoch = 200;
alphas = [1,10];
costs = ["CE"];
lambs = [0,2,5];
show = False
k = 5;

trainNN(folder, numHarmonics, percent_Val, numHidden, batch_size, times, epoch, alphas, costs, lambs, k, False);
