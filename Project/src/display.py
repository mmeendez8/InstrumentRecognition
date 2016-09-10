import sys

##############################################################
#                    Display  functions                      #
#                                                            #
##############################################################

##############################################################
#                    ERROR FUNCTION                          #
#   prints an error in the screen                            #
#   inputs:                                                  #
#           function ==> String of the function in which     #
#                   the error has occured                    #
#      additionalmes ==> String with the message of error    #
#          breakcode ==> Boolean, if it is True, then the    #
#                   program exists and does not run          #  
#                   anymore                                  #
##############################################################

def error(function, additionalmes = "", breakcode = False, show = True):
    mes = 'Error: '
    mes += function;
    mes += " : ";     
    mes += " " + additionalmes;
    if show == True:                       # Bollean to show the message
        print >> sys.stderr, mes
    if breakcode == True:
        sys.exit();

##############################################################
#                  DISPLAY FUNCTION                          #
#   prints a message in the screen                           #
#   inputs:                                                  #
#      message ==> String with the message to be printed     #
##############################################################

def display(message, show = True):
    if show == True:                       # Boolean to show the message
        print message;

##############################################################
#                    DISPLAY NOTE FUNCTION                   #
#   prints an note  in the screen                            #
#   inputs:                                                  #
#           function ==> string of the note to be printed    #
##############################################################

def displayNote(note, show = True):
    if show == True:
        print "NOTE! : " + note;
    

##############################################################
#                    input  functions                        #
#                                                            #
##############################################################

def argument(message = ""):
    message += " : "
    arg = raw_input(message);
    return arg;


    
