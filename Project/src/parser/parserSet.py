import os
import display
import numpy as np

class parserSet:
    def __init__(self, name):
        self.changeName(name);

    def changeName(self, name):
        self.name = name;
        self.directory = os.getcwd() + "/data/sets/";
        self.filename = self.directory + name + ".set";

    def writeHead(self, label,description = ""):
        f = open(self.filename, 'w');
        lineStart = "#########################################################################\n";  # write the first line
        f.write(lineStart);
        f.write("#                                  Set " + self.name);
        linesDescription = 1 + len(description)/ 50; 
        for i in range(linesDescription):                                                           # with a maximum of 50 caracters
            f.write("\n# ");
            for j in range(50):
                if (50*i + j) < len(description):
                    f.write(description[50*i+j]);
                else:
                    f.write("\n");                                                                  # When finish, go to the following line
                    break;
        differentInstruments = self.findDifferentInstruments(label);
        f.write("# Different Instruments / number of samples for each instrument")
        aling = len(max(differentInstruments));
        for i in range(len(differentInstruments)):
            count = 0;
            for j in range(len(label)):
                if label[j] == differentInstruments[i]:
                    count = count + 1;
            f.write("\n# ");
            f.write(differentInstruments[i] + ":");
            for k in range(len(differentInstruments[i]), aling):
                f.write(" ");
            
            f.write(str(count));
        f.write("\n");
        f.write(lineStart);
        f.close();

    def writeData(self, harmonics, label):
        f = open(self.filename, 'a');
        if len(label) == len(harmonics):
            differentInstruments = self.findDifferentInstruments(label);
            outputMatrix = self.createMatrixOutput(label, differentInstruments);
            for i in range(len(label)):
                f.write("\nInstrument: "+ label[i] + "\n");
                f.write("Harmonics:\n");
                for j in range(len(harmonics[i])):
                    f.write(str(harmonics[i][j]) + " ");
                f.write("\nOutput:\n");
                for j in range(len(outputMatrix[i])):
                    f.write(str(int(outputMatrix[i][j])) + " ");
                f.write("\n")
        f.close();

    def write(self, harmonics, label, show = True):
        self.writeHead(label);
        self.writeData(harmonics, label);
        display.displayNote("File saved correctly in: " + self.filename, show);
        

    def read(self, show = True):
        f = open(self.filename, 'r');
        label = [];
        harmonics = [];
        typeFound = False;
        output = [];
        for line in f:
            if line[0] != "#" and line != "\n":
                element = "";
                harm = [];
                out = [];
                for j in range(len(line)):
                    
                    if typeFound == "Harmonics:":
                        if line[j] != " ":
                            element += line[j];
                        else:
                            harm.append(float(element));
                            element = "";
                        if j == len(line) - 1:
                            typeFound = "addHarm";
                            
                    elif typeFound == "Output:":
                        if line[j] != " ":
                            element += line[j];
                        else:
                            out.append(float(element));
                            element = "";
                        if j == len(line) - 1:
                            typeFound = "addOut";
                        
                            
                    else:
                        if line[j] != " " and line[j] != "\n":
                            element += line[j];
                        if element == "Instrument:":
                            typeFound = element;
                            element = "";
                        if element == "Harmonics:":
                            typeFound = element
                            break;
                        if element == "Output:":
                            typeFound = element;
                            break;
                if typeFound == "Instrument:":
                    label.append(element);
                    typeFound = False;
                if typeFound == "addHarm":
                    harmonics.append(harm);
                    typeFound = False;
                if typeFound == "addOut":
                    output.append(out);
                    typeFound = False;
        
        f.close();
        display.displayNote("File loaded correctly from: " + self.filename, show);
        return label, harmonics, output

    def findDifferentInstruments(self, label):
        differentInstruments = [label[0]];
        for i in range(len(label)):
            found = False;
            for j in range(len(differentInstruments)):
                if label[i] == differentInstruments[j]:
                    found = True;
            if found == False:
                differentInstruments.append(label[i]);
        return differentInstruments;


    def createMatrixOutput(self, label, differentInstruments):
        outputMatrix = [];

        for i in range(len(label)):
            output = np.zeros( len(differentInstruments));
            for j in range(len(differentInstruments)):
                if label[i] == differentInstruments[j]:
                    output[j] = 1;
                    output[j] = int(output[j]);
                    break;
            outputMatrix.append(output);
        return outputMatrix;

                
        



        
        
