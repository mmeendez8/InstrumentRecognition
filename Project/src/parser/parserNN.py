import os
import display
from glob import glob
import numpy as np

########################################################################
#                        CLASS parserNN                                #
#   This class will be used to the read and write on the data files    #
#            as well as to obtain the elements saved in it             #
#                                                                      #
########################################################################

class parserNN:

    ######################### CONSTRUCTOR ###########################

    def __init__(self, name):
        self.changeName(name);

    ######################## METHODS ##############################

    def changeName(self, name):
        self.name = name;
        self.directory = os.getcwd() + "/data/neural_network/";
        self.filename = self.directory + name + ".nn";
        

    def writeHead(self, sizes, description = ""):
        f = open(self.filename, 'w');
        lineStart = "#########################################################################\n";  # write the first line
        f.write(lineStart);
        f.write("#                         Neural Network " + self.name);

        linesDescription = 1 + len(description)/ 50; 
        for i in range(linesDescription):                                                           # with a maximum of 50 caracters
            f.write("\n# ");
            for j in range(50):
                if (50*i + j) < len(description):
                    f.write(description[50*i+j]);
                else:
                    f.write("\n");                                                                  # When finish, go to the following line
                    break;
        f.write("# Layers: ");
        for i in range(len(sizes)):
            f.write(str(sizes[i]) + " ");
        f.write("\n");
        f.close();
        

    def writeWeightsAndBiases(self, weights, biases):
        f = open(self.filename, 'a');
        f.write('################################ WEIGHTS ################################');
        for i in range(len(weights)):
            f.write("\n");
            for j in range(len(weights[i])):
                for k in range(len(weights[i][j])):
                    f.write(str(weights[i][j][k]) + " ");
                f.write("\n");

        f.write('################################ BIASES #################################');
        for i in range(len(biases)):
            f.write("\n");
            for j in range(len(biases[i])):
                f.write(str(biases[i][j].tolist()[0]) + " ");
        f.close();

    def write(self,sizes, weights, biases, show = True):
        self.writeHead(sizes);
        self.writeWeightsAndBiases(weights, biases);
        display.displayNote("Neural Network saved correctly in: " + self.filename, show);


    def readHead(self):
        sizes = [];
        
        f = open(self.filename, 'r');
        found = False;
        for line in f:
            if line[0]!="#":
                break;
            element = "";
            for j in range(len(line)):
                if (line[j] != "#")and(line[j] != ":")and(line[j] != "\n"):
                    element +=line[j];
                if element == " Layers":
                    found = True;

            if found:
                element = element.replace(" Layers ","",1);
                num = ""
                for i in range(len(element)):
                    if element[i] != " ":
                        num += element[i];
                    else:
                        sizes.append(int(num));
                        num = "";
                break;
        f.close();
        return sizes;

    def readWeightsAndBiases(self):
        f = open(self.filename, 'r');
        found = False;

        weights = [];
        biases = [];
        layer = 0;
        rows = 0;
        rowsBias = 0;
        weights.append([]);
        for line in f:
            if line[0]=="#":
                element = "";
                for j in range(len(line)):
                    if (line[j] != " ")and(line[j] != "#")and(line[j] != ":")and(line[j] != "\n"):
                        element += line[j];
                    if element == "WEIGHTS":
                        found = element;
                    if element == "BIASES":
                        found = element;
            if (found == "WEIGHTS")and(line == "\n"):
                weights.append([]);
                layer += 1;
                rows = 0;
            if (found == "WEIGHTS")and(line[0]!= "#")and(line!= "\n"):
                weights[layer].append([]);
                num = "";
                for j in range(len(line)):
                    if (line[j]!= " "):
                        num += line[j];
                    else:
                        weights[layer][rows].append(float(num));
                        num = "";
                        
                rows += 1;
            if (found == "BIASES")and(line[0]!="#")and(line!="\n"):
                biases.append([]);
                num = "";
                for j in range(len(line)):
                    if (line[j]!= " "):
                        num += line[j];
                    else:
                        biases[rowsBias].append([float(num)]);
                        num = "";

                rowsBias += 1;         
        f.close();
        weightsNp = [];
        biasesNp = [];

        
        for i in range(len(weights)):
            weightsNp.append(np.array(weights[i]));       
            biasesNp.append(np.array(biases[i]));

        return weightsNp, biasesNp;

    def read(self, show = True):
        size = self.readHead();
        [weights, biases] = self.readWeightsAndBiases();
        display.displayNote("Neural Network loaded correctly from: " + self.filename, show);

        return size, weights, biases;
    
                
                
        
        
                    
        
        
                
        
