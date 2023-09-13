# Robovac
The main repo for Team 1's CS499 project

## Setting up your dev environment
We will be using python 11 with Pygame, Tkinter, and any other libraries we end up using

> **To make sure all of our environments are the same, we will use something called `Miniconda`. This will allow us to use a fresh environment without worrying about what other python things we have installed**

### Install and update Miniconda
Go [here](https://docs.conda.io/en/latest/miniconda.html) to install the correct Miniconda version for your system **Make sure you acccept the default settings**

On Windows, launch the program called Anaconda prompt. This will be your terminal

![Anaconda Prompt Image](Documentation/AnacondaPrompt.png)

On Mac and Linux, just use your default terminal for all terminal commands

### Create a new Conda environment
This will create a new conda enviroment with all of the packages that we will use
Currently the only Package we have to install seperately is:
-   Pygame

In your terminal, run 

```
conda create --name robovac -c conda-forge Pygame
```
Confirm with `y`

Then to switch to the new environment, run

```
conda activate robovac
```

to test that it worked, run

```
python -m pygame.examples.aliens
```
and 
```
python -m tkinter
```
If both of these work, you are good to go!