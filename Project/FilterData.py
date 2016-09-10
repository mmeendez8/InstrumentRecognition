import sys
sys.path.append("./src");                               # Append source folder
sys.path.append("./src/parser");
import glob
import os
import wav
from pydub import AudioSegment          # import pydub to convert mp3 to wav
import time
import matplotlib.pyplot as plt
import dataset as s
from shutil import copy2


def IsInRange(value, rangValue):
    if value >= rangValue[0] and value < rangValue[1]:
        return True;
    else:
        return False;

def compute_tone(frequency):
    num_scales = 10
    freq  = [16.351598, 17.323914, 18.354048, 19.445436, 20.601722, 21.826764, 23.124651, 24.499715, 25.956544, 27.500000, 29.135235, 30.867706];
    tones = ["C",  "Cs",  "D",  "Ds","E",  "F",   "Fs",  "G","Gs","A", "As",  "B"];
    n= ""
    for i in range(1, num_scales + 1):
        for note in range(len(tones)):
            if i == 1 and tones[note] == "C":
                minrang = 0;
            elif i == 1 and tones [note] != "C":
                minrang = freq[note] - float(freq[note]- freq[note-1])/float(2)
                
            elif i == 2 and tones[note] == "C":
                minrang = pow(2,i-1)*freq[note] - float(pow(2,i-1)*freq[note] - freq[11] )/float(2);
            elif i > 2 and tones[note] == "C":
                minrang = pow(2,i-1)*freq[note] - float(pow(2,i-1)*freq[note] - pow(2,i-2)*freq[11] )/float(2);
            else:
                minrang =  pow(2,i-1)*freq[note] - float(pow(2,i-1)*freq[note]- pow(2,i-1)*freq[note-1])/float(2);

            if i == 1 and tones[note] != "B":
                maxrang = freq[note] + float(freq[note+1]- freq[note])/float(2);
            elif i==1 and tones[note] == "B":
                maxrang = freq[note] + float(2*freq[0]- freq[note])/float(2);
            elif i == num_scales and tones[note] == "B":
                maxrang = pow(2,i-1)*freq[note] + float(pow(2,i-1)*freq[note] - pow(2,i-1)*freq[note-1])/2
            elif i != num_scales and tones[note] == "B" and i != 1:
                maxrang = pow(2,i-1)*freq[note] + float(pow(2,i)*freq[0]- pow(2,i-1)*freq[note])/float(2);
            else:
                maxrang = maxrang = pow(2,i-1)*freq[note] + float(pow(2,i-1)*freq[note+1]- pow(2,i-1)*freq[note])/float(2);
            rang = [minrang, maxrang];
            if IsInRange(frequency, rang):
                n = tones[note] + str(i-1);
    if n == "":
        n = "unknown"
    return n

def mp3_2wav(filename):
    file_out = filename.replace(".mp3", ".wav");
    sound = AudioSegment.from_mp3(filename);
    sound.export(file_out, format = "wav");
    return file_out


def compute_volume(amplitude):
    if IsInRange(amplitude, [0, 2500]):
        return "pp";
    if IsInRange(amplitude, [2500, 3500]):
        return "p"
    if IsInRange(amplitude, [3500, 4000]):
        return "mp"
    if IsInRange(amplitude, [4000, 4500]):
        return "mf"
    if IsInRange(amplitude, [4500, 5500]):
        return "f"
    if IsInRange(amplitude, [5500, 100000]):
        return "ff"
    
def extract_tone_from_name(name):
    tones = ["C",  "Cs",  "D",  "Ds","E",  "F",   "Fs",  "G","Gs","A", "As",  "B"];
    num_scales = 10
    for octave in range(num_scales):
        for tone in tones:
            note = tone + str(octave);
            if note in name:
                return note;
            
    


def FilterFiles(directory_in, directory_out):
    print "Filtering files from:"
    print directory_in
    print "to"
    print directory_out
    numFiles =  len(glob.glob(directory_in + '*.mp3'))
    count = 1;
    for filename in glob.glob(directory_in + '*.mp3'):
        progress = float(count)/float(numFiles);
        progress_before = float(count-1)/float(numFiles);
        s.update_progress(progress, progress_before)
        count += 1

        try:
            file_wav = mp3_2wav(filename);
            w = wav.wav(file_wav, "", True)

            amplitude = w.FindMaxAmplitude();
            frequency = w.frequency();

            name = filename.replace(directory_in, "");
            name = name.replace(".mp3", "");
            #print "last name: ", name
            instrument =  s.InstrumentFromName(name)
            tone_freq = compute_tone(frequency);
            volume = compute_volume(amplitude[0]);
            tone_name = extract_tone_from_name(name);

            #print "Freq tone:", tone_freq, "'Actual' tone:", tone_name

            if tone_freq == tone_name:
                tone = tone_freq
                newname = instrument + '_' + tone + '_' + volume;
                index = 1;
        
                newFilename = directory_out + newname + '.mp3';
                if os.path.isfile(newFilename):
                    newname = newname + '_';
                while True:
                    if os.path.isfile(newFilename):
                        newname = newname.replace("(" + str(index-1) + ")", "");
                        newname = newname + "(" + str(index) + ")";
                        newFilename = directory_out + newname + '.mp3';
                        index += 1;
                    else:
                        break
                copy2(filename, newFilename);
                #print "new name:  ", newname
                #print ""

            os.remove(file_wav)
        except:
            pass
    numFiles_in =  len(glob.glob(directory_in + '*.mp3'))
    numFiles_out =  len(glob.glob(directory_out + '*.mp3'))
    print "Taken the " + str(int(float(numFiles_out)/float(numFiles_in)*100)) + "% of the files"


folder = "tuba"
directory_in = os.getcwd() + '/samples/original_datasets/' + folder + '/'
directory_out = os.getcwd() + '/samples/filtering_dataset/' +  folder +  '/'
FilterFiles(directory_in, directory_out);















        
