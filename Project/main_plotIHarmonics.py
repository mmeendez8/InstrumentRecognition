import matplotlib.pyplot as plt
import sys
sys.path.append("./src");                               # Append source folder
sys.path.append("./src/parser")

import wav                                              # Import library wav to treat with the mp3 files
import FourierSeries as FS;
import dataset
import display
import os
import glob
import random

def plotFilename(FileName, folder, harmonics = 20):

    w = wav.wav(FileName, folder);                                  # Create the class wav
    w.cutOptimalInterval();                                 # Cut the wave in an optimal interval of time
    figw = w.plotWav();                                            # Plot the wave

    f = FS.FourierSeries(FileName, folder);
    f.harmonics(10)
    fig = f.plotHarmonics();
    fig.savefig('./figures/harmonics/same_instrument/harmonics_' + FileName);
    return figw;

def get_files(folder):
    directory  = os.getcwd()                                                 # Get current directory
    filesFolder = directory + '/samples/' + folder + '/mp3/';
    files = []
    display.displayNote("Plotting the instrument " + instrument + " from folder /samples/" + folder);
    label = [];
    for filename in glob.glob(filesFolder + '*.mp3'):
        filename = filename.replace(filesFolder, "", 1);
        filename = filename.replace(".mp3", "", 1);
        files.append(filename);
        label.append(dataset.InstrumentFromName(filename));

    return files, label

def plot_same_instrument(folder, instrument, numPlots = 4):

    files, label = get_files(folder)

    maximumPlots = 4;
    count = 0;

    while True:
        i = random.randint(0, len(label)-1);
        if instrument == label[i]:
            
            figw = plotFilename(files[i], folder);
            count += 1;
        if count == maximumPlots:
            break;

    plt.figure(1);
    plt.legend(loc='upper left')
    figw.savefig('./figures/harmonics/same_instrument/interval_' + instrument);



def plot_different_instruments(folder, instruments):

    files, label = get_files(folder)
    
    for instrument in instruments:
        while True:
            i = random.randint(0, len(label)-1);
            if instrument == label[i]:
                figw = plotFilename(files[i], folder);
                break
    plt.figure(1);
    plt.legend(loc='upper left')
    figw.savefig('./figures/harmonics/different_instruments/interval_many_instr');
    
    


folder = "A3"
instrument = "viola"

plot_same_instrument(folder, instrument);
#instruments = ["viola", "clarinet", "bass-clarinet", "trumpet"]

#plot_different_instruments(folder, instruments)






#plt.show()
