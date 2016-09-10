import sys
sys.path.append('./src')
sys.path.append('./src/parser');
import glob
import os
from shutil import copy2
import random
def create_set(num_samples, directory_in, directory_out):
    print "Create set from";
    print directory_in
    print "in"
    print directory_out
    num_files = 0;
    numFiles = len(glob.glob(directory_in + '*.mp3'))
    prob = float(num_samples)/numFiles;
    for filename in glob.glob(directory_in + '*.mp3'):
        p = random.uniform(0,1);
        if p <= prob:
            newname = filename.replace(directory_in, "");
            copy2(filename, directory_out + newname);
            num_files += 1;
    print "Files copied: ", num_files;



directory_in = "/home/andres/Desktop/CI2015/samples/filtering_dataset/violin/"
directory_out = "/home/andres/Desktop/CI2015/samples/11Instruments/mp3/"
num_samples = 300;
create_set = create_set(num_samples, directory_in, directory_out);
print ""
