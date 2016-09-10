import time

import sys
sys.path.append('./parser');

import matplotlib.pyplot as plt
import nn
import dataset
import random
import numpy as np



def trainNN(folder, numHarmonics, percent_Val, numHidden,batch_sizes, times, epoch, alphas, costs, lambs, k, show):

    d = dataset.dataset();

    try:
        filename = "Set_" + folder;
        d.loadSet(filename);
    except:
        d.generateSetFromFolder(folder, numHarmonics);

    data, label, numOutput = d.getData()
    random.shuffle(data)


    folds = []
    for i in range(1,k+1):
        folds.append(data[int((i-1)*len(data)/k):int(i*len(data)/k)]);

    #train = data[indexVal:]
    #validation = data[:indexVal]

    start = time.clock()

    count = 1;
    for hidden in numHidden:
        if hidden != 0:
            NN = nn.nn([numHarmonics, hidden, numOutput] ,folder);
        else:
            NN = nn.nn([numHarmonics, numOutput] ,folder);
        for c in costs:
            NN.cost_name = c
        
            for lambda_ in lambs:
                NN.lambda_ = lambda_

                for batch_size in batch_sizes:
                
                    for alpha in alphas:
                        alpha_ = float(alpha)/len(data);
                    
                        title = "hidden: " +  str(hidden) + ", batch: "+ str(batch_size) + ", fun: " + c + ", lambda: " + str(lambda_) + ", alpha: " + str(alpha);
                        print ""
                        print title

                        sumcosts_train_times = np.zeros(epoch)
                        sumcosts_val_times   = np.zeros(epoch)
                        sumAccs_train_times  = np.zeros(epoch)
                        sumAccs_val_times    = np.zeros(epoch)
                        acc_test = 0;
                    
                        
                        for t in range(times):
                            print "----> Time:",  t

                            sumcosts_train = np.zeros(epoch)
                            sumcosts_val   = np.zeros(epoch)
                            sumAccs_train  = np.zeros(epoch)
                            sumAccs_val    = np.zeros(epoch)
                            acc_test_fold = 0;
                            for i in range(len(folds)):
                                NN.reset()
                                print "      ----> Fold: ", i+1
                                test_data = folds[i];
                                train_data = [];
                                for j in range(len(folds)):
                                    if j != i:
                                        for sample in folds[j]:
                                            train_data.append(sample);
                        
                                random.shuffle(train_data);
                                index = int(float(percent_Val)/100*len(train_data));
                                validation_data = train_data[:index];
                                train_data = train_data[index:];
                            
                                NN.training(train_data, epoch, batch_size, alpha_ ,validation_data, show);


                                sumcosts_train = np.add(sumcosts_train, NN.cost)
                                sumcosts_val   = np.add(sumcosts_val, NN.cost_validation);
                                sumAccs_train  = np.add(sumAccs_train, NN.accuracy_train);
                                sumAccs_val    = np.add(sumAccs_val, NN.accuracy_validation);
                                acc_test_fold += NN.accuracy(test_data);
                    
                            sumcosts_train_times = np.add(sumcosts_train_times, np.true_divide(sumcosts_train, k));
                            sumcosts_val_times   = np.add(sumcosts_val_times, np.true_divide(sumcosts_val  , k));
                            sumAccs_train_times  = np.add(sumAccs_train_times, np.true_divide(sumAccs_train , k));
                            sumAccs_val_times    = np.add(sumAccs_val_times, np.true_divide(sumAccs_val   , k));
                            acc_test += np.true_divide(acc_test_fold, k);

                        sumcosts_train_times = np.true_divide(sumcosts_train_times, times);
                        sumcosts_val_times   = np.true_divide(sumcosts_val_times  , times);
                        sumAccs_train_times  = np.true_divide(sumAccs_train_times , times);
                        sumAccs_val_times    = np.true_divide(sumAccs_val_times  , times);
                        acc_test = np.true_divide(acc_test, times);

                    

                        NN.plotCost(sumcosts_train_times, "Training", 2*count-1, title);
                        fig = NN.plotCost(sumcosts_val_times, "Validation", 2*count-1, title + "  Test Acc = " + str(round(acc_test,1)) + '%');

                        plt.figure(2*count-1);
                        plt.legend(loc='upper left')

                 
                    
                        fig.savefig('./figures/'+folder+'/cost_' + str(hidden) + '_' + str(batch_size) + '_' + c + '_'+ str(lambda_)+ '_'+ str(alpha)+'.png');
                        plt.close(fig);

                        NN.plotAccuracy(sumAccs_train_times,"Training", 2*count, title);
                        fig = NN.plotAccuracy(sumAccs_val_times,"Validation", 2*count, title + "  Test Acc = " + str(round(acc_test,1)) + '%');

                        plt.figure(2*count);
                        plt.legend(loc='upper left')

                        fig.savefig('./figures/'+folder+'/acc_' + str(hidden) + '_' + str(batch_size) + '_' + c + '_'+ str(lambda_)+ '_'+ str(alpha)+'.png');
                        plt.close(fig)


                        count += 1
   
    elapsed = (time.clock() - start)
    print "Time required: ", elapsed, " seconds"
    return elapsed
