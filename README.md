# Greenblatt Script
Script for downloading stock screen information from Joel Greenblatt's Magic Formula Investing (MFI) site. It's assumed you already have an account with Magic Formula Investing. If not, sign up for one now.

## Installation
Run bash script to build Virtual Environment, install python packages and create local settings file:

`sh setup.sh`

## Add Information to Local Settings
For obvious reasons, you don't want your MFI information in a remote location. So add your `EMAIL` and `PASSWORD` credentials to the newly created `settings_local.py` file so you can use them without accidentally uploading them to github. As well, if you'd like to utilize a specific `MIN_MARKET_CAP` number, add it there as well. Otherwise this value will be a randomly generated number between 30-100.

## Download Chrome Driver
Download ChromeDriver the following URL, and make sure to un-zip it within the directory where you've cloned this script: https://sites.google.com/chromium.org/driver/downloads?authuser=0

If you're using a Mac, you may receive the error message: '"chromedriver" cannot be opened because the developer cannot be verified.'

The solution is to make Mac OS trust chromedriver binary:

    xattr -d com.apple.quarantine chromedriver

## Start Virtual Environment
`source venv/bin/activate`

## Download Stock Prices as CSV File
`python download_stocks.py --settings=settings_local`

Stock information should now be available within the newly created csv/ directory.
