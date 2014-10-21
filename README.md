This plugin provides basic thermodynamic cycle modeling tools for OpenMDAO. It's main feature
is the inclusion of a FlowStation variable that provides access to isentropic flow relationships.

# Pre-Reqs


### OpenMDAO 
This is an OpenMDAO plugin, so we assume you have already installed a version of OpenMDAO. 

#### Mac OS-X Tip
On OS-X it is strongly suggested that you setup Python, and other OpenMDAO pre-reqs with 
homebrew. You can follow these [detailed instructions](http://www.lowindata.com/2013/installing-scientific-python-on-mac-os-x/)
but once you have homebrew installed and setup, here is the short version: 


    brew install git
    brew install python
    brew install gfortran
    pip install numpy
    pip install scipy
    brew install freetype
    pip install matplotlib


### Cantera
In addition, this plugin requires [Cantera](http://sourceforge.net/projects/cantera/files/cantera/2.0.2/cantera-2.0.2.tar.gz/download)
and the python wrapper for it. Because of some backwards incompatible changes made to the most recent 
versions of Cantera, you need to install version 2.0.2, and not the latest version. 

You can [compile cantera from scratch](http://cantera.github.io/docs/sphinx/html/compiling.html), 
or follow the instructions below for a bit easier route on windows. 


#### Windows
Cantera provides [pre-compiled](https://code.google.com/p/cantera/downloads/list) binaries 
that are by far the easiest choice for windows. You should follow their instructions 
for the best way to install it and make sure it works. 

But note that you need to install version 2.0.2 and **NOT** the 2.1 beta version. Get only the official 
release version of it! 

https://code.google.com/p/cantera/wiki/WindowsInstallation

#### Mac OS-X

You'll need to compile from source here. Unfortunately, installing Cantera on OS-X is a bit of a mess.  
You can use homebrew to get some of the pre-requisites, but at least one of them needs to be downloaded manually first

first 
    brew tap homebrew/science

Next go to the [sundials page](http://computation.llnl.gov/casc/sundials/download/download.php) and download 
sundials-2.5.0.tar.gz. You need to manually put the zip file you just downloaded in 

    /Library/Caches/Homebrew/sundials-2.5.0.tar.gz

Now you're ready to install the cantera pre-reqs: 

    brew install sundials
    brew install scons

After that, go unzip the [Cantera source code](http://sourceforge.net/projects/cantera/files/cantera/2.0.2/cantera-2.0.2.tar.gz/download) code you downwloaded. GO into that folder and edit a file called cantera.conf with the following lines: 

    CXX = 'llvm-g++'
    CC = 'llvm-gcc'
    python_package = 'full'
    f90_interface = 'n'
    cxx_flags = '-ftemplate-depth-128 -DGTEST_USE_OWN_TR1_TUPLE=1'

Save that file, then run 
    
    scons build

If that works, you'll see something like this in the terminal 

    *******************************************************
    Compilation completed successfully.

    - To run the test suite, type 'scons test'.
    - To install, type '[sudo] scons install'.
    *******************************************************

To finish the install, 
   
   scons install


#### Linux
You're best bet is to follow the [official instructions](http://cantera.github.io/docs/sphinx/html/compiling.html). 


# Installation
Make sure you're in an activated OpenMDAO environment. Then you have two options: 

## Regular install
This will install the plugin, but you won't have access to the source in order to mess around with it. 

    plugin install --github pycycle


## Source install
If you want to have access to the source and make changes to it while you're working then you should do 
an install from source. Don't be scared by the cantera source install though, compared to that this is pretty 
easy! It's only two steps. 

1)Clone the repository to your local machine. If you want to clone ours: 
    
    git clone https://github.com/OpenMDAO-Plugins/pyCycle.git
    

Or you can fork it and clone that to your local machine. Either way... 

2) cd into the pyCycle directory
    
    python setup.py develop
    

