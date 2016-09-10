import matplotlib.pyplot as plt
import os
import sys
sys.path.append("./src");
sys.path.append("./src/parser");
import nn
import dataset
import numpy as np

#os.chdir("../")

import time


filename = "xor"
numHarmonics = 0;
percent_Val = 10;
numHidden = [2];
batch_size = [20];
times = 1000;
epoch = 100;
alphas = [0.1];
costs = ["CE"];
lambs = [0,2,5];
show = False
k = 0;

trainNN(folder, numHarmonics, percent_Val, numHidden, batch_size, times, epoch, alphas, costs, lambs, k, False);
