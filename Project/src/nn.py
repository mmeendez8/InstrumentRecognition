from __future__ import division
import parserNN
import random
import numpy as np
import display
import matplotlib.pyplot as plt

class nn(object):

    def __init__(self, sizes=None, folder="C5", cost_name="CE", lambda_=0):
        FileName = folder + "_nn"
        self.p = parserNN.parserNN(FileName);
        self.num_layers = 0;
        self.sizes = [];
        self.biases = [];
        self.weights = [];
        self.cost = [];
        self.cost_name = cost_name
        self.actv = 'sigmoid'
        self.lambda_ = lambda_
        if sizes != None:
            self.num_layers = len(sizes)
            self.sizes = sizes
            self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
            self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

    #########################################################################
    #                            RESET FUNCTION                             #
    #     Resets the weights and bias following a gaussian distribution     #
    #########################################################################
    def reset(self):
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    #########################################################################
    #                   CHANGEFILENAME FUNCTION                             #
    #      Allows to change the file where the NN parameters will be stored #
    #########################################################################
    def changeFileName(self, name):
        self.p.changeName(name);

    #########################################################################
    #                           LOAD FUNCTION                               #
    #           Loads a previously NN configuration from a file             #
    #########################################################################
    def load(self, show = True):
        [self.sizes, self.weights, self.biases] = self.p.read(show);
        self.num_layers = len(self.sizes);

    #########################################################################
    #                           SAVE FUNCTION                               #
    #              Save the NN configuration into a file                    #
    #########################################################################
    def save(self, show = True):
        self.p.write(self.sizes, self.weights, self. biases, show);
    
    #########################################################################
    #                          FEEDFORWARD FUNCTION                         #
    #           This function feeds the network and gets its output         #
    #########################################################################
    def feedforward(self, x):
        level = 0
        for b, w in zip(self.biases, self.weights):
            if self.actv == 'sigmoid':
                x = sigmoid(np.dot(w, x)+b)
            if level == len(self.weights)-1:
                x = softmax(np.dot(w, x)+b)
        level+=1
        return x

    #########################################################################
    #                          TRAINING FUNCTION                            #
    #           Trains the NN, using mini-batch gradient descent            #
    #########################################################################
    def training(self, training_data, epochs, batch_size, alpha,
            validation_data=None,show = False):
        self.cost = [];
        self.cost_validation = [];
        self.accuracy_train = [];
        self.accuracy_validation = [];

        n = len(training_data)                                                                  # Get sizes of the input
        if validation_data:
            random.shuffle(validation_data)
            n_validation = len(validation_data)

        for j in xrange(epochs):
            tmp = 0                                                                             # Temporal var for summing costs
            tmp_validation = 0
            random.shuffle(training_data)                                                       # Randomly shuffle input data
            batches = [training_data[k:k+batch_size] for k in xrange(0, n, batch_size)]
            for batch in batches:
                self.update(batch, alpha,batch_size)
            for x,y in training_data:                                                             # Store cost in order to plot
                tmp += self.costFunction(self.feedforward(x),y)                                        # Compute the cost for each epoch
            if self.lambda_ != 0:
                l2norm = np.sum(np.linalg.norm(w)**2 for w in self.weights)
                tmp += self.lambda_/(2*n) * l2norm
            self.cost.append(1.0/(2*len(training_data)) *tmp)
            acc_train = self.accuracy(training_data)
            if validation_data:
                for x,y in validation_data:
                    tmp_validation += self.costFunction(self.feedforward(x),y);
                if self.lambda_ != 0:
                    l2norm = np.sum(np.linalg.norm(w)**2 for w in self.weights)
                    tmp_validation += self.lambda_/(2*n_validation) * l2norm

                self.cost_validation.append(1.0/(2*len(validation_data))*tmp_validation);
                acc_val   = self.accuracy(validation_data);
                display.displayNote("Iteration {0}: Proportion of well classified samples: Train: {1}  Validation: {2}".format(
                    j, acc_train, acc_val), show);
                self.accuracy_train.append(acc_train);
                self.accuracy_validation.append(acc_val);
            else:
                
                display.displayNote("Iteration {0}: Training samples classified: {1}".format(
                    j, acc_train),show);
                self.accuracy_train.append(acc_train);


    #########################################################################
    #                          UPDATE FUNCTION                              #
    #        Updates the weights and biases of the networks after each      #
    #           minibatch based on backpropagation algorithm results        #
    #########################################################################
    def update(self, batch, alpha,n):
        gradw = [np.zeros(w.shape) for w in self.weights]
        gradb = [np.zeros(b.shape) for b in self.biases]
        for x, y in batch:
            deltab, deltaw = self.backpropagation(x, y)
            gradb = [nb+db for nb, db in zip(gradb, deltab)]
            gradw = [nw+dw for nw, dw in zip(gradw, deltaw)]                                    # For applying regularization set lambda_!= 0
        reg_term = alpha*(self.lambda_/n)
        self.weights = [w - reg_term*w - alpha*nw for w, nw in zip(self.weights, gradw)]        # Update weights
        self.biases = [b-alpha*nb for b, nb in zip(self.biases, gradb)]                         # Update bias


    #########################################################################
    #                     BACKPROPAGATION FUNCTION                          #
    #    Uses backpropagation algorithm to compute how weights and biases   #
    #        of the NN should change in order to adapt to the solution      #
    #########################################################################
    def backpropagation(self, x, y):
        deltab = [np.zeros(b.shape) for b in self.biases]                                       # Set initial matrix to zero
        deltaw = [np.zeros(w.shape) for w in self.weights]

        activation = x                                                                          # Output of the first layer = input
        activations = [x]                                                                       # List to store all the activations, layer by layer
        zs = []                                                                                 # list to store all the z vectors, layer by layer
        level = 0
        for b, w in zip(self.biases, self.weights):                                             # Select weight and bias for one layer
            z = np.dot(w, activation)+b                                                         # Compute w*x+b
            zs.append(z)
            if level == len(self.weights)-1:
                activation = softmax(z)                                                         # APply sigmoid for the last layer
            else:
                activation = sigmoid(z)                                                         # Apply sigmoid function
            activations.append(activation)
            level += 1
                                                                                                # Go backwards on the network
        delta = self.cost_derivative(activations[-1], y)                                        # Last layer delta
        if self.cost_name == "MSE":
            delta = delta * sigmoid_derivative(zs[-1])
        deltab[-1] = delta                                                                      # Compute db and dw for the last layer
        deltaw[-1] = np.dot(delta, activations[-2].transpose())

        for l in xrange(2, self.num_layers):                                                    # Compute them for the other layers
            z = zs[-l]
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sigmoid_derivative(z)
            deltab[-l] = delta
            deltaw[-l] = np.dot(delta, activations[-l-1].transpose())
        return (deltab, deltaw)

    #########################################################################
    #                          ACCURACY FUNCTION                            #
    #       Computes how many instance have been correctly classified       #
    #########################################################################
    def accuracy(self, data):
        count = 0;
        for x, y in data:
            result = np.zeros(len(y));
            result[np.argmax(self.feedforward(x))] = 1;                                         # Set 1 the position of the max returned value from the NN
            correct = True;
            for i in range(len(y)):
                if y[i][0] != result[i]:                                                        # When NN result == true result -> +1 accuracy
                    correct = False;
                    break;
            if correct == True:
                count += 1;
        acc = float(count)/len(data)*100
        
        return acc;


    #########################################################################
    #                           COST FUNCTION                               #
    #       This function computes the cost whit the selected method        #
    #########################################################################
    def costFunction(self, a, y):
        tmp = 0
        if self.cost_name == "CE":                                                               # Cross-Entropy
            tmp = np.sum(np.nan_to_num(-y*np.log(a)-(1-y)*np.log(1-a)))
        elif self.cost_name == "MSE":                                                            # Minimum Squared Error
            tmp = np.sum((pow(y - a,2)))


        return tmp


    #########################################################################
    #                     COST_DERIVATIVE FUNCTION                          #
    #       This function computes the value of the cost derivative for     #
    #                   a given output of the network                       #
    #########################################################################
    def cost_derivative(self, output_activations, y):
            return (output_activations-y)


    #########################################################################
    #                          PLOTCOST FUNCTION                            #
    #               Plots the cost value VS the epoch number                #
    #########################################################################
    def plotCost(self, toplot, cost_data, figNum, title):
        if len(toplot)>0:
            tmp = self.cost
            self.cost = toplot
        if self.cost != []:
            fig = plt.figure(figNum);
            #plt.hold(True);
            plot = []
            for i in range(len(self.cost)):
                plot.append(np.abs(self.cost[i]))
            plt.plot(plot, label = cost_data);
            #plt.axis([0, len(self.cost), 0, 1])
            plt.xlabel("Epochs");
            plt.ylabel("Cost Function");
            plt.title("Cost: " + title)
            plt.legend()
            return fig
        if tmp: self.cost = tmp

    #########################################################################
    #                          PLOTACCURACY FUNCTION                        #
    #               Plots the cost value VS the epoch number                #
    #########################################################################
    def plotAccuracy(self, accuracy, accuracy_name, figNum, title):
        if len(accuracy) > 0:
            fig = plt.figure(figNum)
            #plt.hold(True);
            plt.plot(accuracy, label = accuracy_name);
            plt.ylim([0, 100]);
            plt.xlabel("Epoch");
            plt.ylabel("Accuracy");
            plt.title("Accuracy: " + title);
            return fig;

# Activation functions

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

def sigmoid_derivative(z):
    return sigmoid(z)*(1-sigmoid(z))

def softmax(z):
    return np.true_divide(np.exp(z), np.sum(np.exp(z)))
