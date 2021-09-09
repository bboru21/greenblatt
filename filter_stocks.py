import pandas
import argparse


parser = argparse.ArgumentParser(
    description='Parses Robinhood trades CSV file',
)
parser.add_argument(
    '--nrows',
    type=int,
    help='nrows argument for pandas.read_csv',
    default=None,
)

args = parser.parse_args()
nrows = args.nrows


df = pandas.read_csv(
    'csv/robinhood.csv',
    header=0,
    nrows=nrows,
    delimiter="|",
    # error_bad_lines=False,
)

print(df)
print('finis')