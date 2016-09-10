from scipy import integrate
import wav
import numpy as np
import matplotlib.pyplot as plt

#########################################################################
#                      FOURIERSERIES CLASS                              #
#         Class to Compute the Fourier Serie from a signal              #
#                                                                       #
#########################################################################

class FourierSeries:

    ########################## CONSTRUCTOR ##################################
    #                                                                       #
    #         When the class is inizialized, it is required to input the    #
    #           data file name .wav without the extension, it means         #
    #                only the name. For example if the name of the          #
    #              file .wav is piano.C5.wav, the right way to iniziate     #
    #              the class is:         w = wav('piano.C5')                #
    #   INPUT:                                                              #
    #         filename ==> String Name of the file to be treated WITHOUT    #
    #                      the extension / format ('.wav')                  #
    #########################################################################
    def __init__(self, Filename, folder = "C5"):
        self.folder = folder;
        self.w = wav.wav(Filename, self.folder);                                   # Read the file with the class wav
        self.changeFilename(Filename, self.folder);
        
    ########################## METHODS #####################################

    def changeFilename(self, Filename, folder = ""):
        if folder != "":
            self.folder = folder;
        self.w.changeFilename(Filename, self.folder);
        self.cutPeriodicInterval();                                            # Cut the signal wave into a periodic interval
        self.numHarmonics = 0;                                                 
        self.a = []
        self.b = []
        self.harm = [];                                                        # Define de vector which will contain the harmonics of the signal

        
    #########################################################################
    #                   CUTPERIODICINTERVAL FUNCTION                        #
    #       Cut the signal into a periodic interval given by the period     #
    #          This interval is given by two maximmums of the signal        # 
    #########################################################################  

    def cutPeriodicInterval(self):
        
        [self.period, Times] = self.w.period();                                          # Get the period of the signal
        self.freq = self.w.frequency();                                         # Get the frequency of the signal
        #index = self.w.FindMaxAmplitude()[1];                                   # Get the index of the maximum amplitude                                                                                                                                             # Get the interval of 10 times the wavelength
        #Time1 = self.w.Time[index];                                             # Define the time1 from the maximum amplitude
        #Time2 = Time1 + self.period;                                            # Define the time2 from the time1 + the period
        #self.w.cutWav(Time1, Time2);                                            # Cut the wave between time1 and time2
        self.w.cutWav(Times[0],Times[1]);
        #self.rangTime = max(self.w.Time)- min(self.w.Time);
                                                                                # Normalize the time between 0 and 1
        #self.Time   = np.true_divide(self.w.Time - min(self.w.Time), self.rangTime);
        #self.period = (self.period)/self.rangTime                               # Normalize period 
        self.Time = self.w.Time - min(self.w.Time);
        self.freq = 2*np.pi/self.period                                         # and frequency
        self.w.signal = 0.5*self.w.signal;
        self.rang = np.array(max(self.w.signal)-min(self.w.signal), dtype='int64');                      # Normalize the signal between -1 and 1
        self.signal = -1 + 2*np.true_divide(self.w.signal - min(self.w.signal),self.rang)

    #########################################################################
    #                         HARMONICS FUNCTION                            #
    #       Compute the harmonic terms of the signal. The number of         #
    #           harmonics is given by the user as input                     #
    #        INPUT:                                                         #
    #              numberHarmonics -> Number of harmonic terms in the serie #
    ######################################################################### 

    def harmonics(self, numberHarmonics):
        self.numHarmonics = numberHarmonics
        self.a = []
        self.b = []
        for i in range(numberHarmonics):
            w_i = self.freq*i;                                                  # Compute each harmonic frequency
            cos = np.cos(w_i*self.Time);                                        # Compute cos(w_i * t)
            sin = np.sin(w_i*self.Time);                                        # Compute sin(w_i * t)
            function_a = np.multiply(self.signal, cos);                         # Compute cos(w_i * t) * f(t)  (f(t) is the signal)
            function_b = np.multiply(self.signal, sin);                         # Compute sin(w_i * t) * f(t)  (f(t) is the signal)
            self.a.append((2/self.period)*integrate.simps(function_a, self.Time));# Compute the terms of the cos
            self.b.append((2/self.period)*integrate.simps(function_b, self.Time));# Compute the terms of the sin
        self.a[0] = self.a[0]/2;                                                 # Divide by 2 the term a_0
        self.harm = np.sqrt(np.square(self.a)+np.square(self.b));               # Compute the harmonics as c_n = sqrt(a_n^2 + b_n^2)
    
        
    #########################################################################
    #                    PLOT HARMONICS FUNCTION                            #
    #   This function plots the real signal and the series approximation    #
    #       in the first subplot and the harmonics values in the second     #
    #                             subplot                                   #
    #########################################################################         
    def plotHarmonics(self):
        fig = plt.figure()                                                           # Create new figure
        ay1 = plt.subplot(121);                                                # Create subplot for the plot of the left
        plt.title('Signal Wave of ' + self.w.filename);                        # Set title
        ay1.plot(self.Time, self.signal,'b', label = "Real signal")                                   # Plot signal vs Time
        plt.xlabel('Time (seconds)');
        plt.ylabel('Amplitude');
        plt.hold(True);                                                        # Hold the actual plot
        serie = np.zeros(len(self.Time));                                      # Allocate in memory the serie of the signal with 0s
        for i in range(self.numHarmonics):                                     # Loop for all the harmonics computed
            w_i = self.freq*i;                                                 # Compute the frequency of each harmonic
            cos = np.cos(w_i*self.Time);                                       # Compute cos(w_i * t)
            sin = np.sin(w_i*self.Time);                                       # Compute sin(w_i * t)
            function = self.a[i]*cos + self.b[i]*sin                           # Compute a_n * cos + b_n * sin
            serie += function;                                                 # Sum the result to the serie
        ay1.plot(self.Time, serie,'r', label ="Wave from harmoncis");                                        # Plot the serie in red
        plt.legend(loc='upper left')
        
        ay2 = plt.subplot(122);                                                # Create other subplot for the harmonics
        x = np.arange(0,len(self.harm));                                       # Create x-axis
        plt.title('Harmonics: [ 0 - ' + str(self.numHarmonics -1) + " ]");     # Set title
        ay2.bar(x,self.harm);                                                  # Plot with bars the harmonics
        plt.ylim((0,1));                                                       # Set the range of the y-axis in [0,1]
        plt.xlabel('Harmonic number');
        plt.ylabel('Amplitude');
        return fig;
        
        

    
            


            
