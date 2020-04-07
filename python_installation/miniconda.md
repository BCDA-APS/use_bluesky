# Install Miniconda

These instructions describing installation of either a
Miniconda or Anaconda Python distribution, providing
the [`conda`](https://docs.conda.io) virtual environment management tool.

CONTENTS

- [Install Miniconda](#install-miniconda)
  - [Download](#download)
  - [Choose an installation location](#choose-an-installation-location)
  - [Run the installer](#run-the-installer)

## Download

Download an installer for Python v3.  
(Python v2 was end-of-life 2019-12-31.)

Given the choice between Anaconda and Miniconda, use *Anaconda* if you 
want a full-featured base environment.  Choose *Miniconda* for a minimal 
base environment (which makes it easier to upgrade and manage the 
additional conda environment we'll use for bluesky).  Your choice.

TIP:  With Miniconda, you usually do not add additional packages to 
the base environment.  Instead, you'd create custom conda environments, as needed.
Smaller, more specific environments make it easier to manage the
dependencies (including python version) required to run certain Python applications.

distribution  | instructions
---- | ----
[Anaconda](https://www.anaconda.com/distribution/#download-section) | click the green button for "Python 3.7 version" (64-bit) for your operating system
[Miniconda](https://repo.anaconda.com/miniconda/) | pick the `Miniconda3-latest-*` installer for your operating system and architecture

Then, save the installer file (goes into your `Downloads` folder on most operating systems).

## Choose an installation location

NOTE: 
The installer will ask you in which directory to install.  This is 
usually a great choice.  The installer will create this directory, do 
not create it in advance.  However, the parent directory must exist.

The parent directory in which you install Python (Anaconda or Miniconda) is your decision.
You should consider if you are installing just for your account or any account
on your computer, or even for a networked installation.

For my personal use, I create an `Apps` parent directory under my HOME 
directory where I install major software such as this.

TIP:
Choose a parent directory with *no embedded whitespace* and only 
ASCII characters in the entire path text.

## Run the installer

Run the installer file.  It may be an executable installer or it may need to 
be run from the command-line with: `bash INSTALLER.sh` 
(see the instruction provided with the installer).

For the most part, take the defaults unless you have a different choice.

The installer will ask you at the end if it should activate the conda base environment
by default when you start your command-line console.  This is your choice.  
For me, I agree to this request.
