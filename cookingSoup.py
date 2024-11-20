import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--medals',action='store_true', help = 'show medalists of the chosen cuntry')
parser.add_argument('country', type= str)
parser.add_argument('year', type= str)

args = parser.parse_args()

print(args)

with open('/Users/olenakoshel/Documents/GitHub/assignment-3-tomatosoup/Olympic Athletes - raw.tsv', encoding="utf-8") as f:
    lines = f.readlines()

column_names = lines[0].strip().split('\t')

data = [dict(zip(column_names, line.strip().split("\t"))) for line in lines[1:]]

def filter(country, year):

    # country = input("Enter ur country or code: ").strip()
    # year = str(input("Enter ur year: ").strip())
    # year = str(year)
    got_medals = [{"Name": olimpian["Name"], "Event": olimpian["Event"], "Medal": olimpian["Medal"]}
        for olimpian in data
        if (olimpian["Team"].lower() == country.lower() or olimpian["NOC"].lower() == country.lower()) and olimpian["Year"] == year and olimpian["Medal"] != "NA" ]
    print("Top Medalists:")
    for olimpian in got_medals[:10]:
        print(f"{olimpian['Name']} - {olimpian['Event']} - {olimpian['Medal']}\n")
if args.medals:
    filter(args.country, args.year)




