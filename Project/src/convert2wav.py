from pydub import AudioSegment          # import pydub to convert mp3 to wav
import os                               # import os to get the current directory
import display as d                     # import display to print errors

#########################################################################
#                      CONVERT2WAV FUNCTION                             #
#         Convert a file from .mp3 to wav and save it in the folder     #
#      ./samples/C5_mp3 with the same name as the original file but     #
#                        with extension .wav in stead of .mp3           #
#   INPUT:                                                              #
#         filename ==> String Name of the file to be converted WITHOUT  #
#                      the extension / format ('.mp3')                  #
#         Format ====> String Format of the file that is going to be    #
#                      converted. By default is .mp3                    #
#   OUTPUT:                                                             #
#         output ===> Boolean. True if the file has been converted      #
#                              False otherwise                          #
#########################################################################

def convert2wav(filename, folder = "C5", Format = 'mp3'):
    directory  = os.getcwd()                                                 # Get current directory
    inputFile  = directory + '/samples/' + folder + '/mp3/' + filename + '.' + Format;   # load the complete name of the mp3 file
    outputFile = directory + '/samples/' + folder + '/wav/' + filename + '.wav';        # load the complete name of the wav file
    output = False                                                           # set the output false
    try:                                                                     # Try to convert the file
        sound = AudioSegment.from_mp3(inputFile)                             # to wav, and if so, then 
        sound.export(outputFile, format="wav")                               # output is true
        output = True
        d.displayNote("Successful")
    except:                                                                  # otherwise print error
        d.error('convert2wav()', 'The file could not be converted', True)

    return output                                                            # return the result as true or false
    
    
