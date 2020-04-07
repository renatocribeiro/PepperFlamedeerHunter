# PepperFlamedeerHunter
Bounty hunter for pepper.com based websites.


# Usage
Download the latest [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it in the root of the project.
Create the conda environment and activate it:
```
conda env create -f environment.yml
conda activate pepper
```
Add the websites you want to use on `Agents.py` and the user(s) details on `Users.py`.

To launch the script use `python main.py`.

### Flags

`--only-dump` dumps the current collection(s) into `.json` files.

`--debug` opens all the browser's instances in UI mode (headless by default)

# Disclaimer
Use at your own risk. This repository/project is intended for personal/educational purposes only. Scripts provided AS-IS.
