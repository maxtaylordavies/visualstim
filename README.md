# visualstim

## Getting started

1. clone this repo: `git clone https://github.com/maxtaylordavies/visualstim.git` and `cd visualstim`
2. create conda environment: `conda env create -f environment.yml`
   - if this fails, you can add the required packages manually with `conda install -c conda-forge pywinhook` and then `conda install -c conda-forge psychopy`
   - you can verify the package installations with `conda list` - you should see (amongst other things) `psychopy 2021.2.3`
3. run `python test.py` to see the GUI
