# This document contains the instructions to install the required packages to run the QTrobovac project

This project runs best on Python 3.12.

To ensure that there are no conflicts, I recommend using Conda to manage your python environments

## How to install Conda
Go [here](https://docs.conda.io/en/latest/miniconda.html) to install the correct Miniconda version for your system **Make sure you acccept the default settings**

On Windows, launch the program called Anaconda prompt. This will used for all of your conda, pip, and python commands

![Anaconda Prompt Image](Documentation/AnacondaPrompt.png)

On Mac and Linux, just use your default terminal for all terminal commands

### Create a new Conda environment
Create a new conda environment to install the required packages in. To do this, run

```conda create --name robovac python==3.12```

Confirm with `y`

Then to switch to the new environment, run

```conda activate robovac```

## Install packages
Next, install the required packages.
In your new environment, run
```pip install pyqt5 numpy matplotlib opencv-python```

This will install all of the required packages to run the project.

# How to run the project
To run the project, run runProject.py, which is at the root of the Source folder.
You may need to make sure that you are in the correct directory. To get there, run
```cd <Path To Robovac\Source>```

then run

```python runProject.py```

# How to use Robovac
Robovac has 3 modules, Floorplan Designer, Simulator, and ViewPreviousRuns.

You can you use the Floorplan Designer to create a floor plan for Robovac to clean. 

You can use the Simulator to simulate Robovac cleaning a floor plan.

You can use ViewPreviousRuns to view the results of previous runs.


### If you're looking for instructions on how to develop Robovac, go [here](HowToDevelop.md)