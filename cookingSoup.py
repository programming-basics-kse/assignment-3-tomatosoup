import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-m', '--medals',action='store_true', help = 'show medalists of the chosen country')
parser.add_argument('-output', type=str)
parser.add_argument('-total', action='store_true')
parser.add_argument('country', type= str, nargs= '?')
parser.add_argument('year', type= str, nargs='?')
parser.add_argument('-overall', nargs='+')
parser.add_argument('-interactive', action='store_true')

args = parser.parse_args()

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
                f.write(f"no medalists found for {country} in {year}.\n")
        return

    print("first 10 medalists:")

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
        
def total(year):

    medals_by_country = {}

    for olimpian in data:

        if olimpian["Year"] == year and olimpian["Medal"] != "NA":
            country = olimpian["Team"]

            if country not in medals_by_country:
                medals_by_country[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}

            medals_by_country[country][olimpian["Medal"]] += 1

    if not medals_by_country:

        print(f"No medals were awarded in {year}.")

        if args.output:
            with open(args.output, 'w', encoding="utf-8") as f:
                f.write(f"No medals were awarded in {year}.\n")

        return

    print(f"Medals summary for {year}:")

    for country, medals in medals_by_country.items():
        print(f"{country} - Gold: {medals['Gold']}, Silver: {medals['Silver']}, Bronze: {medals['Bronze']}")

    if args.output:
        with open(args.output, 'w', encoding="utf-8") as f:
            for country, medals in medals_by_country.items():
                f.write(f"{country} - Gold: {medals['Gold']}, Silver: {medals['Silver']}, Bronze: {medals['Bronze']}\n")



def best_games_of_country(country):

    medals_year_specific = {}

    country_medals = [
        olimpian for olimpian in data
        if ((olimpian["Team"] and olimpian["Team"].lower() == country.lower()) or
            (olimpian["NOC"] and olimpian["NOC"].lower() == country.lower())) and
        olimpian["Medal"] != "NA"
    ]

    if not country_medals:

        print(f"No medals found for {country}.")

        return


    for olimpian in country_medals:

        year = olimpian["Year"]
        medals_year_specific[year] = medals_year_specific.get(year, 0) + 1

    best_year = max(medals_year_specific, key=medals_year_specific.get)
    worst_year = min(medals_year_specific, key=medals_year_specific.get)

    least_medals = medals_year_specific[worst_year]
    most_medals = medals_year_specific[best_year]

    print(f"{country} - {best_year} - {most_medals} medals {worst_year} - {least_medals} medals ")



def analyze_overall(countries):

    for country in countries:
        best_games_of_country(country)

def interactive_mode():

    while True:
        country = input("Enter a country (or type 'exit' to quit): ").strip()

        if country.lower() == 'exit':
            print("Exiting interactive mode.")
            break

        country_data = [
            olimpian for olimpian in data
            if ((olimpian["Team"] and olimpian["Team"].lower() == country.lower()) or
                (olimpian["NOC"] and olimpian["NOC"].lower() == country.lower()))
        ]

        if not country_data:

            print(f"No data found for {country}.")

            continue

        first_year = min(country_data, key=lambda x: int(x["Year"]))
        first_year_place = first_year["City"]

        medals_year_specific = {}

        for olimpian in country_data:
            if olimpian["Medal"] != "NA":
                year = olimpian["Year"]
                medals_year_specific[year] = medals_year_specific.get(year, 0) + 1

        if not medals_year_specific:
            print(f"{country} has no medal records.")
            continue

        best_year = max(medals_year_specific, key=medals_year_specific.get)
        worst_year = min(medals_year_specific, key=medals_year_specific.get)

        avg_gold = sum(1 for olimpian in country_data if olimpian["Medal"] == "Gold") / len(set(olimpian["Year"] for olimpian in country_data))
        avg_silver = sum(1 for olimpian in country_data if olimpian["Medal"] == "Silver") / len(set(olimpian["Year"] for olimpian in country_data))
        avg_bronze = sum(1 for olimpian in country_data if olimpian["Medal"] == "Bronze") / len(set(olimpian["Year"] for olimpian in country_data))

        print(f"""
        Country: {country}
        First Olympics: {first_year["Year"]} in {first_year_place}
        Best Year: {best_year} ({medals_year_specific[best_year]} medals)
        Worst Year: {worst_year} ({medals_year_specific[worst_year]} medals)
        Average Medals per Olympics:
            Gold: {avg_gold:.2f}, Silver: {avg_silver:.2f}, Bronze: {avg_bronze:.2f}
        """)

if args.medals:

    if args.country and args.year:
        filter(args.country, args.year)
    else:
        print("Country and year are required for the -m/--medals command.")

elif args.total:

    year = args.year

    if args.country and args.country.isdigit():  
        year = args.country
    if year:
        total(year)
    else:
        print("Year is required for the -total command.")

elif args.overall:
    analyze_overall(args.overall)

elif args.interactive:
    interactive_mode()

else:
    print("No valid command provided.")

# こんばんは　
