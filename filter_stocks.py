import pandas
import argparse
import json


parser = argparse.ArgumentParser(
    description='Parses Robinhood trades CSV file',
)
parser.add_argument(
    '--nrows',
    type=int,
    help='nrows argument for pandas.read_csv',
    default=None,
)
parser.add_argument(
    '--write',
    action='store_true',
    help='write parsed dataframe to excel sheet',
)

args = parser.parse_args()
nrows = args.nrows
write = args.write


df = pandas.read_csv(
    'csv/robinhood.csv',
    header=0,
    nrows=nrows,
    converters={
        'executed_notional': json.loads,
        'total_notional': json.loads,
    },
    quotechar="'",
)

if write:
    df.to_excel('csv/robinhood-parsed.xlsx')

print('finis')
