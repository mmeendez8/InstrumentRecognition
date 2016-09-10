#########################################################################
#                  Install packages required for the program            #
#########################################################################


class setup:
    def __init__(self):
        self.install('wave');
        self.install('scipy');
        self.install('pydub');
        self.install('Tkinter');
        self.install('matplotlib');
    
    def install(self, package):
        import importlib                       # Import importlib to import packages
        try:
            importlib.import_module(package)   # Try to import the package input
        except ImportError:                    # If the package is not installed,
            import pip                         # then install the package with pip
            pip.main(['install', package])


# Execute in terminal by:
# cd CI2015
# sudo python setup.py

setup()
