import glob
import os
import FourierSeries as FS
import re
import sys
import numpy as np
import parserSet
import display

class dataset:
    def __init__(self):
        self.files = [];
        self.TrainMatrix = [];
        self.label = [];
        self.differentInstruments = [];
        self.harmonics = [];
        self.p = parserSet.parserSet("");
        
    def generateSetFromFolder(self, folder, numharmonics = 10):
        directory  = os.getcwd()                                                 # Get current directory
        filesFolder = directory + '/samples/' + folder + '/mp3/';
        files = []
        display.displayNote("Generating the data set from folder /samples/" + folder);
        for filename in glob.glob(filesFolder + '*.mp3'):
            filename = filename.replace(filesFolder, "", 1);
            filename = filename.replace(".mp3", "", 1);
            files.append(filename);

        f = FS.FourierSeries(files[0], folder);
        TrainMatrix = [];
        instrument  = [];
        label = [];
        for i in range(len(files)):
            progress_before = float(i-1)/float((len(files)-1));
            progress = float(i)/float((len(files)-1));
            #print progress
            update_progress(progress, progress_before);
            lab = InstrumentFromName(files[i]);
            if lab != "undefined":
                f.changeFilename(files[i], folder);
                f.harmonics(numharmonics);
                TrainMatrix.append(f.harm);
                label.append(lab);
        
        differentInstruments = self.p.findDifferentInstruments(label);
        outputMatrix = self.p.createMatrixOutput(label, differentInstruments);
        self.files = files;
        self.harmonics = TrainMatrix;
        self.label = label;
        self.differentInstruments = differentInstruments;
        self.outputMatrix = outputMatrix

        name = "Set_" + folder;
        self.saveSet(name,  TrainMatrix, label);


    def getData(self):
        differentInstruments = self.p.findDifferentInstruments(self.label);
        outputMatrix = self.p.createMatrixOutput(self.label, differentInstruments);

        data = [];
        harmonics = []
        output = []
        for i in range(len(self.harmonics)):
            harm = []
            out = [];
            for j in range(len(self.harmonics[i])):
                harm.append([self.harmonics[i][j]]);
            harmonics.append(np.array(harm));

            for j in range(len(outputMatrix[i])):
                out.append([outputMatrix[i][j]]);
            output.append(np.array(out));
            data.append((harmonics[i], output[i]));
                

        numOutput = len(output[0]);
        return data, self.label, numOutput;


    def loadSet(self, filename, show = True):
        self.p.changeName(filename);
        [label, harmonics, outputMatrix] = self.p.read(show);
        self.harmonics = harmonics;
        self.label = label;
        self.differentInstruments = self.p.findDifferentInstruments(label);
        self.outputMatrix = outputMatrix;
        
    def loadFolder(self, folder, show = True):
        filename = "Set_" + folder;
        self.loadSet(filename, show);

    def saveSet(self, filename,  harmonics, label, show = True):
        self.p.changeName(filename);
        self.p.write(harmonics, label, show);
        


def update_progress(progress, progress_before):
    
    barLength = 50 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    if int(progress*100) != int(progress_before*100):      
        block = int(round(barLength*progress))
        text = "\rPercent: [{0}] {1}% {2}\n".format( "#"*block + "-"*(barLength-block), int(progress*100), status)
        sys.stdout.write(text)
        sys.stdout.flush()
    

    

def InstrumentFromName(name):
    name = name.lower();
    instruments = ['banjo', 'bass-clarinet', 'cello', 'clarinet', 'flute', 'guitar', 'oboe', 'sax', 'trombone', 'trumpet', 'tuba', 'viola', 'violin']
    for instrument in instruments:
        if instrument in name:
            return instrument
   
