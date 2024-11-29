import argparse
from classanalyzer import OlympicsAnalyzer
with open('/Users/olenakoshel/Documents/GitHub/assignment-3-tomatosoup/Olympic Athletes - raw.tsv', encoding="utf-8") as f:
    lines = f.readlines()
column_names = lines[0].strip().split('\t')
data = [dict(zip(column_names, line.strip().split("\t"))) for line in lines[1:]]
analyzer = OlympicsAnalyzer(data)
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--medals',action='store_true', help = 'show medalists of the chosen country')
parser.add_argument('-output', type=str)
parser.add_argument('-total', action='store_true')
parser.add_argument('country', type= str, nargs= '?')
parser.add_argument('year', type= str, nargs='?')
parser.add_argument('-overall', nargs='+')
parser.add_argument('-interactive', action='store_true')

args = parser.parse_args()

if args.medals:

    if args.country and args.year:
        analyzer.filter(args.country, args.year, output=args.output)
    else:
        print("Country and year are required for the -m/--medals command.")

elif args.total:

    year = args.year if args.year else args.country
    if year:
        analyzer.total(year, output=args.output)
    else:
        print("Year is required for the -total command.")

elif args.overall:
    analyzer.analyze_overall(args.overall)

elif args.interactive:
    analyzer.interactive_mode()

else:
    print("No valid command provided.")


