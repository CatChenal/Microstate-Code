# Microstates Analysis

## Reorganization
The Microstate-Code folder is no longer 'flat', but the benefit is that you do not have to move python 
modules around, rather, you define paths to your data and run the analysis from this "analytics" folder.

### New folders: 
 * `analyze` : The source folder; contains python modules that are importable via `from analyze import x`.
 * `notebooks`: Notebooks for computations or tutorials.


### New Notebook:
 * `charg_ms.ipynb`: Provides a start for getting to know MCCE structures; 'MCCE to MD' project.


### New modules:
 * `update_msa.py`:
 Used to obtain the most up-to-date features from `Stable_MCCE/bin/ms_analysis.py`. Usage:
   1. cd to `analyze` folder;
   2. rename existing `ms_analysis.py` to e.g. `ms_analysis.py.old`;
   3. at the command line type: python `update_msa.py` and press enter

 * `__init__.py`: Makes `analyze` importable.

