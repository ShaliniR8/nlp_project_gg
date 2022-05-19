# Project 1
##  Tweet Mining & The Golden Globes

## Tech

- Python
- NLTK
- Pandas
- [Cinemagoer]


## Installation

Install the requirements file in a new environment.

```sh
pip install -r requirements.txt
```
In case of error while installing install these libraries individually.
```sh
pip install pandas
pip install import-ipynb
pip install cinemagoer
pip install nltk
```
!! 2015 dataset could not be pushed into the repo due to size limit. All datasets for testing go into "datasets" directory

## Result
{'2013': {'awards': {'completeness': 0.1108695652173913,
                     'spelling': 0.8228523741417325},
          'hosts': {'completeness': 1.0, 'spelling': 1.0},
          'nominees': {'completeness': 0.013964285714285714,
                       'spelling': 0.10333333333333333},
          'presenters': {'completeness': 0.04358974358974359,
                         'spelling': 0.14102564102564102},
          'winner': {'spelling': 0.34615384615384615}}}


> Note: run `config.py` to create configuration file.

   
   [Cinemagoer]: <https://cinemagoer.github.io/>

