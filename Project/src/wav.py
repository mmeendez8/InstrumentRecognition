import matplotlib.pyplot as plt
import numpy as np
import wave
import os
import display as d
import convert2wav as cw
#########################################################################
#                                WAV CLASS                              #
#         Class to treat with the files .wav. Reads, cuts               #
#                            or plots the wave                          #
#                                                                       #
#########################################################################

class wav:
    
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
    
    
    def __init__(self, Filename, folder = "C5", fullDirectory = False):
        self.signal = [];                                                      # Define vector signal which will contain the amplitude of the wave
        self.Time   = [];                                                      # Define the Time vector which will contain in seconds the time                                   
        self.changeFilename(Filename, folder, fullDirectory);

    ########################## METHODS #####################################

    def changeFilename(self, Filename, folder = "", fullDirectory = False):
        if folder != "":
            self.folder = folder;
        if fullDirectory == False:
            self.filename = Filename                                               # Define the name of the filename                      
            self.file = os.getcwd() + '/samples/' + folder + '/wav/' + self.filename + '.wav'; # Get the complete filename
            self.read();                                                           # Read the file 
        else:
            self.file = Filename;
            self.read()
        
    #########################################################################
    #                         READ FUNCTION                                 #
    #       Try to read the file .wav, and if it doesn't find it, tries     #
    #           to convert the .mp3 file in the folder /Samples/C5_mp3      #
    #                   to .wav and then read the file                      #
    #########################################################################    
        
    def read(self):
        try:
            spf = wave.open(self.file,'r')                                     # Try to read the file
        except:
            d.error('wav.read()', 'file wav not found');                       # If this fails, 
            d.displayNote("Converting the file from mp3 to wav ...");          # convert the file from .mp3 to .wav
            cw.convert2wav(self.filename, self.folder);            
            spf = wave.open(self.file,'r')                                     # read now the file .wav created
            
        self.signal = spf.readframes(-1)                                       # Get the amplitudes of the file as a function of time
        self.signal = np.fromstring(self.signal, 'Int16')
        self.fs = spf.getframerate();                                          # Get the frame rate parameter of the signal
        self.Time = np.linspace(0, np.true_divide(len(self.signal),self.fs), num=len(self.signal))   # Creates the vector of time from the framerate parameter

    #########################################################################
    #                         PLOTWAV FUNCTION                              #
    #           Plots the signal as a function of time                      #
    #########################################################################
    
    def plotWav(self):
           
        fig = plt.figure(1)                                                          # Create new figure
        
        signal = 0.5*self.signal;
        rang = np.array(max(signal)-min(signal), dtype='int64');                      # Normalize the signal between -1 and 1
        signal = -1 + 2*np.true_divide(signal - min(signal),rang)
        Time = self.Time - min(self.Time)
        plt.plot(Time, signal, label = self.filename)                                       # Plot signal vs Time
        plt.xlabel('Time (seconds)');
        plt.ylabel('Amplitude');

        return fig;
    #########################################################################
    #                   FINDMAXAMPLITUDE FUNCTION                           #
    #      Finds the maximum amplitude of the signal and the position       #
    #                     in the vector (the index )                        #
    #   OUTPUT:                                                             #
    #                  MaxAmp -> Maximum Amplitude value                    #
    #                  index  -> Position in the vector signal of MaxAmp    #
    ######################################################################### 

    def FindMaxAmplitude(self):
        MaxAmp = max(self.signal);                                             # Get maximum Amplitude
        index = self.findIndex(self.signal, MaxAmp, '==');                     # Get the index
        return MaxAmp, index;                                                  # Return them

    #########################################################################
    #                         PERIOD FUNCTION                               #
    #                 Gets the  the time between two consecutive            #
    #                          maximums of amplitude                        #
    #        OUTPUT:                                                        #
    #                 per-> period of the signal in seconds                 #
    ######################################################################### 

    def period(self):
        gotPeriod = False;
        factor = 0.96
        while True:
            index = self.FindMaxAmplitude()[1];                                   # Get the index of the maximum amplitude
            TimesInterval = [];
            numeroMaximos = 0;
            begin = index;
            lastMaximum = self.signal[index];
            try:
                for i in range(begin, len(self.signal)):                              # Loop to read the signal from the maximum amplitude
                    if self.comprobateMaximum(self.signal, i, lastMaximum, factor):
                        lastMaximum = self.signal[i];
                        numeroMaximos = numeroMaximos + 1
                        if numeroMaximos > 20:
                            a = self.Time[i];
                            TimesInterval.append(self.Time[i]);
                    
                    if len(TimesInterval) == 2:                                            # If the interval has the lower and higher limits, then break
                        gotPeriod = True;
                        break;
            except:
                pass;
            if gotPeriod:
                break;
            factor = factor - 0.03;
            
        
        #per = interval[1] - interval[0];                                      # Compute the period from the difference of the lower and higher limits
        per = TimesInterval[1] - TimesInterval[0];
        return [per, TimesInterval];                                                    # returns the period

    def comprobateMaximum(self, signal, index, maxAmplitude, factor):
        maximum = True;
        for j in range(index-5, index):
            if signal[j] >= signal[index]:
                maximum = False;
        for j in range(index + 1, index + 5):
            if signal[j] > signal[index]:
                maximum = False;
        if maximum == True:
            if signal[index] < factor*maxAmplitude:
                maximum = False;
        return maximum;
    
    #########################################################################
    #                         FREQUENCY FUNCTION                            #
    #         Gets the frequency from the time between two consecutive      #
    #                          maximums of amplitude                        #
    #        OUTPUT:                                                        #
    #               freq ->      freq of the signal in Hz                   #
    #########################################################################
    def frequency(self):
        [per, Times]  = self.period();
        freq = float(1)/float(per);                                                    # Compute the frequency from the period
        return freq



    #########################################################################
    #                   CUTOPTIMALINTERVAL FUNCTION                         #
    #         Cut the wave signal in such a optimal way that it is shown    #
    #           only a interval from the maximum amplitude of the signal    #
    #                and 10 times of wavlength from there                   #  
    ######################################################################### 

    def cutOptimalInterval(self):
                                                                                                    
        [per, Times] = self.period();                                                  # Get the wavelength of the signal
        
        interval = 3*per;                                                    # Get the interval of 10 times the wavelength
        Time1 = Times[0];                                             # Define the time1 from the maximum amplitude
        Time2 = Time1 + interval;                                            # Define the time2 from the time1 + the interval
        self.cutWav(Time1, Time2);                                            # Cut the wave between time1 and time2
        

    #########################################################################
    #                         CUTWAV FUNCTION                               #
    #         Cut the wave signal between a minimum and maximum time        #
    #                               in seconds                              #
    #       INPUT:                                                          #
    #              minimum -> lower Limit of the time in SECONDS to cut the #
    #                         signal                                        #
    #              maximum -> higher limit of the time in SECONDS to cut    #
    #                         the signal                                    #
    #########################################################################

    def cutWav(self, minimum, maximum):             
        if minimum >= 0 and minimum < maximum and maximum <= np.true_divide(len(self.signal),self.fs):
                                                                              # If the range [minimum, maximum] in time is correct,

            lowIndex  = self.findIndex(self.Time, minimum, '>=');             # find the index of the lower limit in time
            highIndex = self.findIndex(self.Time, maximum);                   # find the index of the higher limit in time
            self.Time   = self.Time[lowIndex: highIndex];                     # redefine Time between the two indexes found before
            self.signal = self.signal[lowIndex: highIndex];                   # redefine signal between the two indexes found before
            
        else:
            d.error('wav.cutWav()', 'The range [minimum, maximum] is incorrect')


            
    #########################################################################
    #                         FINDINDEX FUNCTION                            #
    #   Find the index of an element in an array defining a operation       #
    #       INPUT:                                                          #
    #              array -> vector in which the value is going to be found  #
    #              value -> value that is going to be found in the vector   #
    #           operator ->                                                 #
    #                      - '<=': the element found in the vector array    #
    #                           is less or equal than the value             #
    #                      - '>=': the element found in the vector array    #
    #                           is more or equal than the value             #
    #                      - '==': the element found in the vector array is #
    #                            equal to the value                        #
    #      OUTPUT:                                                          #
    #              index: Position of the element found in the vector array #
    #                                                                       #
    ######################################################################### 

    def findIndex(self, array, value, operator = '<='):
        for i in range(len(array)):                       # Loop for all the elements in the array
            if operator == '<=':                          # If operator is '<=' find the element less or 
                if array[i] <= value:                     # equal than the value
                    index = i;
            if operator == '>=':                          # if operator is '>=' find the element higher or
                if array[i] >= value:                     # equal to the value
                    index = i;
                    break;
            if operator == '==':                          # If operator is '==' find the element equal to
                if array[i] == value:                     # the value
                    index = i;
                    break;
        return index;                                     # return index
            
        

    
    
