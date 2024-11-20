import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--medals',action='store_true', help = 'show medalists of the chosen cuntry')
parser.add_argument('-output', type=str)
parser.add_argument('country', type= str)
parser.add_argument('year', type= str)

args = parser.parse_args()

print(args)

with open('/Users/olenakoshel/Documents/GitHub/assignment-3-tomatosoup/Olympic Athletes - raw.tsv', encoding="utf-8") as f:
    lines = f.readlines()

column_names = lines[0].strip().split('\t')

data = [dict(zip(column_names, line.strip().split("\t"))) for line in lines[1:]]

def filter(country, year):

    got_medals = [{"Name": olimpian["Name"], "Event": olimpian["Event"], "Medal": olimpian["Medal"]}
        for olimpian in data
        if (olimpian["Team"].lower() == country.lower() or olimpian["NOC"].lower() == country.lower()) and olimpian["Year"] == year and olimpian["Medal"] != "NA" ]
    
    if not got_medals:
        print(f'no medalists found for {country} in {year}')
        if args.output:
            with open(args.output, 'w', encoding="utf-8") as f:
                f.write(f"No medalists found for {country} in {year}.\n")
        return

    print("Top Medalists:")

    results = []
    for olimpian in got_medals[:10]:
        result_line = f"{olimpian['Name']} - {olimpian['Event']} - {olimpian['Medal']}\n"
        results.append(result_line)
        print(result_line)

        number_of_medals_per_country = {"Gold": 0, "Silver": 0, "Bronze": 0}

    for olimpian in got_medals:
        number_of_medals_per_country[olimpian["Medal"]] += 1

    summaryLine = f"\nTotal number of medals for {country} in {year} = {number_of_medals_per_country}"
    print(summaryLine)


    if args.output:
        with open(args.output, 'w', encoding="utf-8") as f:
            for line in results:
                f.write(line + '\n')
            f.write(summaryLine + '\n')

if args.medals:
    filter(args.country, args.year)




