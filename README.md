# Greenblatt Script

## Installation
Run bash script to build Virtual Environment, install python packages and create local settings file:

`sh setup.sh`

## Download Chrome Driver
Download ChromeDriver the following URL, and make sure to un-zip it within the script directory: https://sites.google.com/a/chromium.org/chromedriver/

## Start Virtual Environment
`source virtualenv/bin/activate`

## Download Stock Prices as CSV File
`python download_stocks.py --settings=settings_local`